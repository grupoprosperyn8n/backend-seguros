import os
import random
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pyairtable import Table, Api
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# Force Deploy v2

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración Airtable
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not API_KEY or not BASE_ID:
    print("WARNING: AIRTABLE_API_KEY or AIRTABLE_BASE_ID not set")

# Inicializar Tablas
def get_table(table_name):
    if not API_KEY or not BASE_ID:
        return None
    return Table(API_KEY, BASE_ID, table_name)

# Modelos Pydantic
class RatingRequest(BaseModel):
    estrellas: int
    comentario: Optional[str] = ""
    nombre: Optional[str] = "Anónimo"
    servicio: Optional[str] = "Atención General"
    es_cliente: Optional[str] = "No"
    dni: Optional[str] = None
    autoriza_publicar: Optional[bool] = False
    usar_foto: Optional[bool] = False

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def parse_poliza_block(bloque_texto: str) -> list:
    """
    Parsea un bloque de ETIQUETA_POLIZA y extrae toda la información.
    Soporta múltiples pólizas concatenadas separandolas por emojis de estado.
    Retorna una LISTA de diccionarios con la info de cada poliiza encontrada.
    """
    import re
    
    # 1. Limpieza inicial
    if not bloque_texto:
        return []

    # 2. Estrategia de Split: Dividir por emojis de estado que marcan el inicio de un bloque
    # Expresión regular que busca emojis comunes de inicio de bloque
    # (?=...) es un lookahead positivo para mantener el delimitador
    SEPARATORS_PATTERN = r'(?=[✅🔴🟢⏳⚠️❌])' 
    
    posibles_bloques = re.split(SEPARATORS_PATTERN, bloque_texto)
    bloques = [b.strip() for b in posibles_bloques if b.strip()]

    # Si no se encontraron bloques con emojis, tratamos todo como un solo bloque
    if not bloques:
        bloques = [bloque_texto]

    parsed_policies = []
    
    for bloque in bloques:
        p_info = {
            "numero": "",
            "patente": "",
            "tipo_vehiculo": "",
            "categoria": "",
            "vida": False,
            "auxilio": False,
            "estado": "",
            "descripcion_completa": bloque
        }
        
        # Extraer N° POL
        match = re.search(r'N°\s*POL:?\s*(\d+)', bloque, re.IGNORECASE)
        if match:
            p_info["numero"] = match.group(1)
        
        # Extraer Patente
        match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque, re.IGNORECASE)
        if match:
            p_info["patente"] = match.group(1).upper()
        
        # Extraer Tipo de vehículo
        match = re.search(r'[🚗🚙🚛🏍️]\s+([A-ZÁ-Ú]+)', bloque)
        if match:
            tipo = match.group(1).strip()
            if len(tipo) > 2 and tipo not in ["POL"]: 
                p_info["tipo_vehiculo"] = tipo
            
        # Extraer Estado
        if "ANULADA" in bloque:
            p_info["estado"] = "ANULADA"
        elif "VIGENTE" in bloque:
            p_info["estado"] = "VIGENTE"
        
        match_vence = re.search(r'(VENCE\s*\d+D?)', bloque)
        if match_vence:
            p_info["estado"] = match_vence.group(1)
        
        # Extras
        if "VIDA: SI" in bloque or "❤️ VIDA" in bloque:
            p_info["vida"] = True
        if "AUX" in bloque or "🆘" in bloque or "🔧" in bloque:
            p_info["auxilio"] = True
            
        parsed_policies.append(p_info)

    return parsed_policies


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/")
def read_root():
    return {"status": "online", "service": "Linktree Backend Python"}

@app.get("/api/validar-cliente")
async def validar_cliente(dni: str, patente: str):
    """
    Valida si un DNI tiene una póliza activa con la patente indicada.
    Replica la lógica del workflow N8N 'VALIDAR_CLIENTE_SINIESTRO'.
    """
    table_clientes = get_table("CLIENTES")
    if not table_clientes:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    # 1. Buscar Cliente por DNI
    # Fórmula: ({DNI} & "") = "12345678"
    formula = f"({{DNI}} & \"\") = \"{dni}\""
    try:
        records = table_clientes.all(formula=formula, max_records=1)
    except Exception as e:
        print(f"Error Airtable: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to database")

    if not records:
        return {
            "valid": False,
            "reason": "CLIENT_NOT_FOUND",
            "message": f"No encontramos un cliente con el DNI ingresado ({dni}). Verificá que esté escrito correctamente."
        }

    cliente = records[0]["fields"]
    nombre_completo = cliente.get("NOMBRE COMPLETO") or cliente.get("NOMBRES") or "Cliente"
    
    # 2. Obtener compilación de pólizas (Lookup)
    compilacion = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", [])
    
    # Manejar si es string o lista
    texto_polizas = ""
    if isinstance(compilacion, list):
        texto_polizas = " ".join([str(x) for x in compilacion])
    else:
        texto_polizas = str(compilacion or "")

    # 3. Parsear INTELIGENTEMENTE todas las pólizas
    polizas_encontradas = parse_poliza_block(texto_polizas)
    
    patente_buscada = patente.upper().strip()
    poliza_match = None
    
    # Buscar la póliza específica
    for p in polizas_encontradas:
        if p["patente"] == patente_buscada:
            poliza_match = p
            break
            
    if not poliza_match:
         return {
            "valid": False,
            "reason": "PATENTE_NOT_FOUND",
            "message": f"Hola {nombre_completo}, no encontramos el vehículo patente {patente_buscada} asociado a tu DNI."
        }

    # 4. Verificar estado (ANULADA/BAJA)
    estado_poliza = poliza_match.get("estado", "").upper()
    if "ANULADA" in estado_poliza or "BAJA" in estado_poliza:
         return {
            "valid": False,
            "reason": "POLICY_INACTIVE",
            "message": f"La póliza del vehículo {patente_buscada} figura como ANULADA o DE BAJA."
        }

    # Limpieza de descripción (quitar emojis al inicio si existen)
    descripcion = poliza_match.get("descripcion_completa", "").strip()
    for char in ["✅", "⏳", "❌", "⚠️"]:
        descripcion = descripcion.replace(char, "")
    descripcion = descripcion.strip()

    # 5. Obtener Record ID de la Póliza (Crucial para Airtable Linked Record)
    record_id_poliza = None
    ids_polizas = cliente.get("POLIZAS", [])
    
    if ids_polizas:
        try:
            table_polizas = get_table("POLIZAS")
            if table_polizas:
                # Iteramos las pólizas del cliente para encontrar la que coincide con la patente
                # Esto es necesario porque el ID no está en el string compilado
                for pid in ids_polizas:
                    try:
                        pol_record = table_polizas.get(pid)
                        fields_p = pol_record["fields"]
                        # Buscamos patente en campos clave o etiqueta
                        str_fields = str(fields_p.values()).upper()
                        
                        if patente_upper in str_fields:
                            record_id_poliza = pid
                            break
                    except:
                        continue
        except Exception as e:
            print(f"Error fetching poliza details: {e}")

    return {
        "valid": True,
        "message": "Validación exitosa",
        "cliente": {
            "nombres": cliente.get("NOMBRES"),
            "apellido": cliente.get("APELLIDO"),
            "fullname": nombre_completo
        },
        "poliza": {
            "record_id": record_id_poliza,
            "numero": poliza_match.get("numero", "0000"),
            "patente": poliza_match.get("patente", patente_upper),
            "tipo_vehiculo": poliza_match.get("tipo_vehiculo", "VEHICULO"),
            "categoria": poliza_match.get("categoria", ""),
            "vida": poliza_match.get("vida", False),
            "auxilio": poliza_match.get("auxilio", False),
            "estado": poliza_match.get("estado", "DESCONOCIDO"),
            "descripcion_completa": descripcion
        }
    }

@app.get("/api/testimonios")
async def get_testimonios():
    """
    Obtiene testimonios aprobados de la tabla CALIFICACIONES.
    Lógica de Selección:
    - Mix: 70% Buenos (>=3 estrellas), 30% Otros (<3 estrellas).
    - Prioridad: Últimos 3 meses.
    - Fallback: Si no completa cupo con recientes, usa antiguos.
    - Total Objetivo: 10 testimonios.
    """
    table_calif = get_table("CALIFICACIONES")
    if not table_calif:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    # Fórmula: Visible=True, Autoriza=True, Comentario!=''
    # Traemos TODO (sin filtro de fecha en API) para poder hacer el fallback
    formula = "AND({VISIBLE}=TRUE(), {AUTORIZA_PUBLICAR}=TRUE(), {COMENTARIO}!='')"
    
    try:
        records = table_calif.all(formula=formula)
    except Exception as e:
        print(f"Error fetching testimonios: {e}")
        return {"testimonios": [], "total": 0, "mensaje": "Error obteniendo datos"}
    
    if not records:
        return {"testimonios": [], "total": 0, "mensaje": "Sin testimonios disponibles"}

    # Procesar registros y separar por fecha y calificación
    now = datetime.now().astimezone() # Aware
    cutoff_90d = datetime.now().timestamp() - (90 * 24 * 60 * 60) # Timestamp comparison logic easier
    
    pool_recent_good = []
    pool_recent_bad = []
    pool_old_good = []
    pool_old_bad = []

    formatted_map = {} # ID -> Formatted Dict

    for r in records:
        f = r["fields"]
        stars = f.get("ESTRELLAS", 0)
        
        # Parse Date
        date_str = f.get("FECHA DE CREACION") or r.get("createdTime")
        is_recent = False
        
        # Intentar parsear fecha
        try:
            # ISO format from Airtable: 2023-10-25T12:00:00.000Z
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            is_recent = dt.timestamp() >= cutoff_90d
            
            # Texto relativo
            delta = datetime.now(dt.tzinfo) - dt
            days = delta.days
            if days == 0: texto_tiempo = "Hoy"
            elif days == 1: texto_tiempo = "Ayer"
            elif days < 7: texto_tiempo = f"Hace {days} días"
            elif days < 30: texto_tiempo = f"Hace {days // 7} semanas"
            else: texto_tiempo = f"Hace {days // 30} meses"
        except:
            texto_tiempo = "Reciente"
            is_recent = False 

        # Formatear
        nombre = f.get("NOMBRE", "Anónimo")
        
        # Iniciales
        partes = nombre.strip().split()
        if partes:
            iniciales = (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper()
        else:
            iniciales = "?"

        foto_url = None
        if f.get("USAR FOTO") and f.get("FOTO PERFIL"):
            fotos = f.get("FOTO PERFIL")
            if isinstance(fotos, list) and len(fotos) > 0:
                foto_url = fotos[0].get("url")

        item = {
            "id": r["id"],
            "nombre": nombre,
            "iniciales": iniciales,
            "estrellas": stars,
            "comentario": f.get("COMENTARIO", ""),
            "fecha": texto_tiempo,
            "fotoUrl": foto_url
        }
        
        formatted_map[r["id"]] = item
        
        # Clasificar
        if stars >= 3:
            if is_recent: pool_recent_good.append(item)
            else: pool_old_good.append(item)
        else:
            if is_recent: pool_recent_bad.append(item)
            else: pool_old_bad.append(item)

    # Shuffle pools
    random.shuffle(pool_recent_good)
    random.shuffle(pool_recent_bad)
    random.shuffle(pool_old_good)
    random.shuffle(pool_old_bad)

    final_selection = []
    
    # Objetivo: 7 Buenos, 3 Malos/Otros
    target_good = 7
    target_bad = 3
    
    # 1. Fill Bad (30%)
    # - Try Recent Bad
    take_bad = pool_recent_bad[:target_bad]
    final_selection.extend(take_bad)
    needed_bad = target_bad - len(take_bad)
    
    if needed_bad > 0:
        # - Fallback to Old Bad
        take_bad_old = pool_old_bad[:needed_bad]
        final_selection.extend(take_bad_old)
        
    # 2. Fill Good (70%)
    # - Try Recent Good
    take_good = pool_recent_good[:target_good]
    final_selection.extend(take_good)
    needed_good = target_good - len(take_good)
    
    if needed_good > 0:
        # - Fallback to Old Good
        take_good_old = pool_old_good[:needed_good]
        final_selection.extend(take_good_old)
        
    # 3. Fill Remainder (if < 10 total) with ANYTHING left
    # Collect leftovers
    current_ids = {x["id"] for x in final_selection}
    leftovers = []
    
    # Helper to add leftovers
    for pool in [pool_recent_good, pool_old_good, pool_recent_bad, pool_old_bad]:
        for item in pool:
            if item["id"] not in current_ids:
                leftovers.append(item)
                
    random.shuffle(leftovers)
    needed_total = 10 - len(final_selection)
    if needed_total > 0:
        final_selection.extend(leftovers[:needed_total])

    # Final Shuffle for display
    random.shuffle(final_selection)

    return {
        "testimonios": final_selection,
        "total": len(final_selection),
        "mensaje": f"Mostrando {len(final_selection)} opiniones"
    }

@app.get("/api/rating")
async def get_average_rating():
    """
    Calcula el promedio de calificaciones visibles.
    """
    table_calif = get_table("CALIFICACIONES")
    if not table_calif:
        return {"rating": 5.0, "total": 0}
    
    # Formula: VISIBLE=TRUE y ESTRELLAS > 0
    formula = "AND({VISIBLE}=TRUE(), {ESTRELLAS}>0)"
    try:
        records = table_calif.all(formula=formula, fields=["ESTRELLAS"])
    except:
        return {"rating": 0, "total": 0}
        
    if not records:
        return {"rating": 0, "total": 0}
        
    total_stars = sum(r["fields"].get("ESTRELLAS", 0) for r in records)
    count = len(records)
    if count == 0: return {"rating": 0, "total": 0}
    
    average = round(total_stars / count, 1)
    
    return {
        "rating": average,
        "total": count
    }

@app.post("/api/rating")
async def save_rating(data: RatingRequest):
    """
    Guarda una nueva calificación. Vincula cliente si existe.
    """
    table_calif = get_table("CALIFICACIONES")
    table_clientes = get_table("CLIENTES")
    
    if not table_calif:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    # Campos base
    fields = {
        "ESTRELLAS": data.estrellas,
        "CUAL FUE TU EXPERIENCIA CON NOSOTROS": data.estrellas, 
        "NOMBRE": data.nombre,
        "ES_CLIENTE": data.es_cliente,
        "SERVICIO": data.servicio,
        "COMENTARIO": data.comentario,
        "MODO": "Online",
        "VISIBLE": True,
        "AUTORIZA_PUBLICAR": data.autoriza_publicar,
        "USAR FOTO": data.usar_foto,
        "EMPLEADO": ["recrUCS6NhFjVmzqm"] # ID Agente Online
    }

    client_linked = False
    
    # Intentar vincular cliente
    # Intentar vincular cliente
    if data.es_cliente == "Sí" and data.dni:
        # Por defecto asumimos 'No' hasta encontrarlo (Lógica N8N)
        fields["ES_CLIENTE"] = "No" 
        
        # Limpiar DNI (solo dígitos porque en Airtable es NUMBER)
        dni_limpio = "".join(filter(str.isdigit, str(data.dni)))

        if table_clientes and dni_limpio:
            try:
                # Buscar ID del cliente (Campo numérico, sin comillas)
                formula = f"{{DNI}}={dni_limpio}"
                c_records = table_clientes.all(formula=formula, max_records=1)
                
                if c_records:
                    fields["CLIENTE"] = [c_records[0]["id"]]  # Link record
                    fields["ES_CLIENTE"] = "Sí"  # Confirmado
                    fields["DNI"] = int(dni_limpio) # Guardar como número si el campo destino lo permite o string limpio
                    client_linked = True
                else:
                    # No encontrado -> Se mantiene ES_CLIENTE='No'
                    pass
            except Exception as e_airtable:
                print(f"Error buscando cliente en Airtable: {e_airtable}")
                # No fallamos todo el proceso, solo la vinculación
                pass
    
    try:
        record = table_calif.create(fields)
        return {
            "status": "success",
            "message": "Calificación registrada correctamente",
            "recordId": record["id"],
            "clienteVinculado": client_linked
        }
    except Exception as e:
        print(f"Error creando rating: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class SiniestroValidationRequest(BaseModel):
    dni: str
    patente: str

@app.get("/api/validate-siniestro")
async def validate_siniestro(dni: str, patente: str):
    """
    Valida cliente y póliza para el flujo de Siniestros.
    Usa la tabla CLIENTES y el campo ETIQUETA_POLIZA Compilación (de POLIZAS).
    Retorna objeto compatible con app.js Siniestros.
    """
    table_clientes = get_table("CLIENTES")
    
    if not table_clientes:
        raise HTTPException(status_code=500, detail="Airtable config error")
        
    dni_limpio = "".join(filter(str.isdigit, str(dni)))
    patente_limpia = patente.upper().strip().replace(" ", "")
    
    if not dni_limpio or not patente_limpia:
        return {"valid": False, "message": "Datos incompletos"}

    # 1. Buscar Cliente por DNI
    formula = f"({{DNI}} & \"\") = \"{dni_limpio}\""
    try:
        records = table_clientes.all(formula=formula, max_records=1)
    except Exception as e:
        print(f"Error buscando cliente: {e}")
        return {"valid": False, "message": "Error validando cliente"}

    if not records:
        return {"valid": False, "message": "Cliente no encontrado"}

    cliente = records[0]["fields"]
    nombre_completo = cliente.get("NOMBRE COMPLETO") or cliente.get("NOMBRES") or "Cliente"
    
    # 2. Obtener compilación de pólizas (Lookup)
    compilacion = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", [])
    
    # Manejar si es string o lista
    if isinstance(compilacion, list):
        texto_polizas = " | ".join([str(x) for x in compilacion])
    else:
        texto_polizas = str(compilacion or "")

    # 3. Verificar si la patente está en el texto de pólizas
    if patente_limpia not in texto_polizas.upper():
        return {
            "valid": False,
            "message": f"No encontramos el vehículo patente {patente_limpia} asociado a tu DNI."
        }

    # 4. Extraer el bloque completo de la póliza que corresponde a esta patente
    # El formato puede tener múltiples pólizas separadas por pipes.
    # Estrategia: Dividir por '|' y agrupar. Un nuevo grupo empieza cuando detectamos un Estado (✅, ❌, ⏳, ⚠️).
    
    parts = [p.strip() for p in texto_polizas.split("|")]
    bloques_detectados = []
    current_bloque = []
    
    emojis_inicio = ["✅", "❌", "⏳", "⚠️"]
    
    for part in parts:
        # Verificar si este fragmento es el inicio de una nueva póliza (tiene emoji de estado)
        es_inicio = any(e in part for e in emojis_inicio) and ("VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part)
        
        # Caso especial: Si es el primer fragmento, siempre empieza bloque
        if not current_bloque:
            current_bloque.append(part)
        elif es_inicio:
            # Guardar el bloque anterior y empezar uno nuevo
            bloques_detectados.append(" | ".join(current_bloque))
            current_bloque = [part]
        else:
            # Continuar agregando al bloque actual
            current_bloque.append(part)
            
    # Agregar el último bloque procesado
    if current_bloque:
        bloques_detectados.append(" | ".join(current_bloque))
        
    # Buscar cuál de estos bloques contiene la patente
    bloque_match = None
    for bloque in bloques_detectados:
        # Chequeo robusto de patente: que esté la patente y (opcionalmente) el emoji
        if patente_limpia in bloque.upper():
            bloque_match = bloque
            break
            
    # Fallback si no se encontró (usar todo el texto, aunque sea arriesgado)
    if not bloque_match:
        bloque_match = texto_polizas

    # Verificar estado (ANULADA/BAJA) SOLAMENTE en el bloque coincidente
    if "ANULADA" in bloque_match.upper() or "BAJA" in bloque_match.upper():
        return {
            "valid": False,
            "message": f"La póliza del vehículo {patente_limpia} figura como ANULADA o DE BAJA."
        }
    
    # 5. Parsear toda la información de la póliza usando helper
    poliza_info = parse_poliza_block(bloque_match)

    # 6. Obtener Record ID de la Póliza para pre-llenado correcto en Airtable
    # El formulario requiere el ID (rec...) para vincular, no el número de texto.
    record_id_poliza = None
    ids_polizas = cliente.get("POLIZAS", [])
    
    if ids_polizas:
        try:
            table_polizas = get_table("POLIZAS")
            if table_polizas:
                # Iteramos las pólizas del cliente para encontrar la que coincide con la patente
                # Esto es más seguro que buscar en toda la tabla
                for pid in ids_polizas:
                    try:
                        pol_record = table_polizas.get(pid)
                        fields_p = pol_record["fields"]
                        # Buscamos patente en campos clave o etiqueta
                        # Usamos representación string de campos para asegurar match
                        str_fields = str(fields_p.values()).upper()
                        
                        if patente_limpia in str_fields:
                            record_id_poliza = pid
                            break
                    except:
                        continue
        except Exception as e:
            print(f"Error fetching poliza details: {e}")

    # 7. Retornar datos completos
    return {
        "valid": True,
        "cliente": {
            "nombres": cliente.get("NOMBRES", ""),
            "apellido": cliente.get("APELLIDO", ""),
        },
        "poliza": {
            "record_id": record_id_poliza, # ID para Linked Record
            "numero": poliza_info["numero"],
            "patente": poliza_info["patente"],
            "tipo_vehiculo": poliza_info["tipo_vehiculo"],
            "categoria": poliza_info["categoria"],
            "vida": poliza_info["vida"],
            "auxilio": poliza_info["auxilio"],
            "estado": poliza_info["estado"],
            "descripcion_completa": poliza_info["descripcion_completa"]
        }
    }


# ==============================================================================
# CONFIGURACIÓN DINÁMICA DE FORMULARIOS
# ==============================================================================

# ==============================================================================
# CRECIÓN DE SINIESTRO
# ==============================================================================

class SiniestroRequest(BaseModel):
    tipo_formulario: str
    poliza_record_id: str
    datos: dict
    dni: Optional[str] = None
    patente: Optional[str] = None

@app.post("/api/create-siniestro")
async def create_siniestro(request: SiniestroRequest):
    """
    Crea un registro en la tabla correspondiente de Airtable según el tipo de formulario.
    Vincula automáticamente Póliza y Cliente si están disponibles.
    """
    print(f"📝 Recibiendo siniestro: {request.tipo_formulario}")
    
    # 1. Determinar Tabla y Mapeo según Tipo
    table_name = ""
    fields_map = {}
    
    # IMPORTANTE: IDs de tablas y nombres de campos según Metadata
    # Accidente: DENUNCIA DE ACCIDENTE
    # Robo/Incendio: DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL
    # Robo Parcial: CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )
    
    if request.tipo_formulario == "accidente":
        table_name = "DENUNCIA DE ACCIDENTE"
        fields_map = {
            "fecha": "FECHA DEL SINIESTRO",
            "hora": "HORA APROX. DEL SINIESTRO",
            "direccion": "LUGAR O ESTABLECIMIENTO", # O "DIRECCIÓN Y N°"
            "relato": "RELATOS DEL HECHO",
            # "terceros": "HUBO TERCEROS?", # Chequear campo exacto
            # "lesionados": "HUBO LESIONADOS?" # Chequear campo exacto
        }
    elif request.tipo_formulario == "robo-incendio":
        table_name = "DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL"
        fields_map = {
            "fecha": "FECHA DEL HECHO", # Validar nombre
            "hora": "HORA",
            "direccion": "LUGAR DEL HECHO",
            "relato": "RELATO DEL HECHO",
            "tipo_hecho": "TIPO DE HECHO"
        }
    elif request.tipo_formulario == "robo-parcial":
        table_name = "CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )"
        fields_map = {
            "fecha": "FECHA DEL HECHO",
            "direccion": "LUGAR DEL HECHO",
            "relato": "RELATO DEL HECHO",
            "elemento": "ELEMENTO AFECTADO" # Validar nombre
        }
    else:
        raise HTTPException(status_code=400, detail="Tipo de formulario desconocido")

    # 2. Obtener Tabla
    table = get_table(table_name)
    if not table:
         raise HTTPException(status_code=500, detail=f"Tabla no encontrada: {table_name}")

    # 3. Construir Payload para Airtable
    airtable_fields = {}
    
    # Mapear campos dinámicos
    # NOTA: Usamos un mapeo genérico de nombres comunes si no tenemos el exacto, 
    # pero trataremos de usar los que vimos en el esquema.
    
    # Mapeos "Seguros" (comunes a casi todos, ajustar si falla)
    # Fechas: Airtable espera YYYY-MM-DD
    if "fecha" in request.datos:
        airtable_fields["FECHA DEL SINIESTRO"] = request.datos["fecha"] # Nombre standarizado?
        # Override para Robo que puede tener otro nombre
        if request.tipo_formulario != "accidente":
             # En metadata Robo Total tiene "FECHA DEL HECHO"? 
             # Voy a asumir FECHA DEL SINIESTRO si no encuentro otro en el error logs
             # Pero en Accidente es FECHA DEL SINIESTRO.
             pass

    if "hora" in request.datos:
        # Airtable Duration o Text? En Accidente era Duration h:mm
        # Front manda "14:30" o number? Front manda number 0-23 en Accidente.
        # Si es number, formatear a string "HH:00"
        val = request.datos["hora"]
        if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
            airtable_fields["HORA APROX. DEL SINIESTRO"] = f"{int(val):02d}:00"
        else:
            airtable_fields["HORA APROX. DEL SINIESTRO"] = str(val)

    if "direccion" in request.datos:
        airtable_fields["LUGAR O ESTABLECIMIENTO"] = request.datos["direccion"]
        airtable_fields["DIRECCIÓN Y N°"] = request.datos["direccion"] # Llenamos ambos por las dudas

    if "relato" in request.datos:
        # Accidente usa "RELATOS DEL HECHO"
        if request.tipo_formulario == "accidente":
             airtable_fields["RELATOS DEL HECHO"] = request.datos["relato"]
        else:
             # Robo / OC puede usar otro. Intentaremos "RELATO" o "DETALLE"
             airtable_fields["DESCRIPCION"] = request.datos["relato"] # Generico
             # Si falla por campo inexistente, pyairtable avisa.

    # 4. Vincular Póliza (CRITICO)
    if request.poliza_record_id:
        airtable_fields["POLIZAS"] = [request.poliza_record_id]

    # 5. Vincular Cliente (Si tenemos DNI, buscamos ID)
    # Es mejor buscar el cliente fresco por DNI para asegurar el ID correcto
    if request.dni:
        dni_limpio = "".join(filter(str.isdigit, str(request.dni)))
        t_clientes = get_table("CLIENTES")
        if t_clientes and dni_limpio:
            try:
                c_records = t_clientes.all(formula=f"{{DNI}}={dni_limpio}", max_records=1)
                if c_records:
                    airtable_fields["CLIENTE"] = [c_records[0]["id"]]
            except Exception as e:
                print(f"Error vinculando cliente: {e}")

    # 6. Guardar
    try:
        # Filtrar campos que podrían no existir para evitar error 422 estricto??
        # Airtable API v0 devuelve error si el campo no existe.
        # Para ser robustos, en esta fase de desarrollo rapido,
        # podríamos hacer un 'try' con campos específicos si sabemos que varían.
        # Por ahora enviamos lo que creemos standard.
        
        # Ajustes finales de nombres según Metadata leída previamente (Accidente)
        if request.tipo_formulario == "accidente":
            # Campos confirmados en lectura anterior
            pass 
            
        print(f"Enviando a Airtable {table_name}: {airtable_fields}")
        record = table.create(airtable_fields, typecast=True) # typecast=True ayuda con selects y fechas
        return {"status": "success", "id": record["id"], "message": "Denuncia creada correctamente"}
        
    except Exception as e:
        print(f"Error creando registro Airtable: {e}")
        # Retornar error detallado para debug en frontend
        raise HTTPException(status_code=500, detail=f"Error Airtable: {str(e)}")


