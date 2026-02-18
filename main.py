import os
import random
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Body, File, UploadFile, Form, Request
import json
try:
    from .drive_service import upload_file_to_drive
except ImportError:
    from drive_service import upload_file_to_drive
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
    Soporta múltiples pólizas concatenadas separandolas por emojis de estado o palabras clave.
    Estrategia: Dividir por '|' y reagrupar lógicamente.
    """
    import re

    # 1. Limpieza inicial
    if not bloque_texto:
        return []

    # 2. Tokenizar por tubería '|'
    parts = [p.strip() for p in bloque_texto.split("|")]
    bloques_reconstruidos = []
    current_bloque = []
    
    # Emojis/Keywords que marcan inicio de poliza (heurística)
    emojis_inicio = ["✅", "❌", "⏳", "⚠️", "🟢", "🔴", "🟣", "⭕"]
    keywords_inicio = ["VIGENTE", "VENCE", "ANULADA", "BAJA", "ACTIVA", "SIN VIGENCIA", "SIN POLIZAS", "TRAMITES"]

    for part in parts:
        part_upper = part.upper()
        # Es inicio si tiene emoji de estado Y palabras clave de estado
        tiene_emoji = any(e in part for e in emojis_inicio)
        tiene_keyword = any(k in part_upper for k in keywords_inicio)
        
        es_inicio = tiene_emoji and tiene_keyword
        
        # Caso especial: Si es el primer fragmento, empieza bloque
        if not current_bloque:
            current_bloque.append(part)
        elif es_inicio:
            bloques_reconstruidos.append(" | ".join(current_bloque))
            current_bloque = [part]
        else:
            current_bloque.append(part)
            
    if current_bloque:
        bloques_reconstruidos.append(" | ".join(current_bloque))

    parsed_policies = []
    
    for bloque in bloques_reconstruidos:
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
        
        # Extraer N POL — usar [0-9] en vez de d, [ ] en vez de s
        match = re.search(r'N[°][ ]*POL[:]?[ ]*([0-9]+)', bloque, re.IGNORECASE)
        if not match:
            # Fallback: buscar cualquier secuencia de 5+ digitos como numero de poliza pero evitar patentes numericas largas (raro)
            match = re.search(r'([0-9]{5,})', bloque)
        if match:
            p_info["numero"] = match.group(1)
        
        # Extraer Patente con emoji
        # Intentamos capturar lo que sigue al emoji de etiqueta
        match = re.search(r'🏷️?[ ]*([A-Z]{2,3}[0-9]{3}[A-Z]{0,2}|[A-Z0-9]{6,9})', bloque, re.IGNORECASE)
        # Refinamiento: Si hay un emoji "🏷️" explícito, tomamos lo que sigue
        match_explicit = re.search(r'🏷️[ ]*([A-Z0-9]+)', bloque, re.IGNORECASE)
        
        if match_explicit:
             p_info["patente"] = match_explicit.group(1).upper()
        elif match:
             # Validación extra para evitar falsos positivos
             posible_patente = match.group(1).upper()
             # Patentes argentinas viejas (AAA123) o nuevas (AA123BB) o motos (A123BCD)
             # Evitar capturar cosas como "VENCE" o "POL" si el regex es muy laxo
             if len(posible_patente) >= 6 and not posible_patente.startswith("POL"):
                 p_info["patente"] = posible_patente
        
        # Extraer Tipo de vehiculo con emoji auto/moto/camion
        match = re.search(r'[🚗🚙🚛🏍️][ ]+([A-ZÁ-Ú]+)', bloque)
        if match:
            tipo = match.group(1).strip()
            if len(tipo) > 2 and tipo not in ["POL"]: 
                p_info["tipo_vehiculo"] = tipo
        
        # Si no encontro tipo, buscar palabras clave comunes
        if not p_info["tipo_vehiculo"]:
            for tipo_clave in ["AUTOMOVIL", "AUTO", "CAMIONETA", "MOTO", "CAMION", "UTILITARIO", "PICK UP", "PICKUP"]:
                if tipo_clave in bloque.upper():
                    p_info["tipo_vehiculo"] = tipo_clave
                    break
            
        # Extraer Estado
        bloque_upper = bloque.upper()
        if "ANULADA" in bloque_upper:
            p_info["estado"] = "ANULADA"
        elif "VIGENTE" in bloque_upper:
            p_info["estado"] = "VIGENTE"
        elif "SIN VIGENCIA" in bloque_upper:
             p_info["estado"] = "SIN VIGENCIA"
        
        match_vence = re.search(r'(VENCE[ ]*[0-9]+[D]?)', bloque_upper)
        if match_vence:
            p_info["estado"] = match_vence.group(1)
        
        # Extras: Vida y Auxilio
        if "VIDA: SI" in bloque_upper or "❤️ VIDA" in bloque or "VIDA" in bloque_upper:
            p_info["vida"] = True
        if "AUX" in bloque_upper or "🆘" in bloque or "🔧" in bloque:
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
                        
                        if patente_buscada in str_fields:
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
            "patente": poliza_match.get("patente", patente_buscada),
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
    parsed_list = parse_poliza_block(bloque_match)
    # parse_poliza_block retorna una LISTA — tomar el primer elemento
    poliza_info = parsed_list[0] if parsed_list else {
        "numero": "", "patente": patente_limpia, "tipo_vehiculo": "",
        "categoria": "", "vida": False, "auxilio": False,
        "estado": "CONSULTAR", "descripcion_completa": bloque_match
    }

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

@app.get("/api/config-formularios")
async def get_config_formularios():
    """
    Retorna la configuración completa DYNAMIC para el frontend.
    Estructura: { "slug": { "titulo": "...", "campos": [...] } }
    """
    t_forms = get_table("CONFIG_FORMULARIOS")
    t_campos = get_table("CONFIG_CAMPOS")
    
    if not t_forms or not t_campos:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    try:
        # 1. Traer Todos los Formularios
        forms_records = t_forms.all()
        
        # 2. Traer Todos los Campos (Optimizacion: traer todo y filtrar en memoria)
        campos_records = t_campos.all()
        
        config_response = {}
        
        for f_rec in forms_records:
            f = f_rec["fields"]
            codigo = f.get("CODIGO")
            visible = f.get("VISIBILIDAD", False)
            
            if not codigo or not visible: continue
            
            form_id = f_rec["id"]
            
            # Filtrar campos para este formulario
            # El campo "Formulario" en CONFIG_CAMPOS es un array de IDs [RecID]
            my_fields = []
            for c_rec in campos_records:
                c = c_rec["fields"]
                linked_forms = c.get("FORMULARIO") or c.get("Formulario", [])
                if form_id in linked_forms:
                    # Mapear a estructura Frontend
                    campo_front = {
                        "id": c.get("ID CAMPO"),
                        "label": c.get("ETIQUETA"),
                        "type": c.get("TIPO", "text"),
                        "required": c.get("OBLIGATORIO", False),
                        # Opcionales
                        "placeholder": c.get("PLACEHOLDER", ""),
                        "options": c.get("OPCIONES", "").split(",") if c.get("OPCIONES") else [],
                    }
                    # NO exponer COLUMNA AIRTABLE al frontend (info interna)
                    # Limpieza de None
                    campo_front = {k: v for k, v in campo_front.items() if v is not None}
                    
                    # Agregar orden si existe para sortear despues
                    campo_front["_orden"] = c.get("ORDEN", 999)
                    
                    my_fields.append(campo_front)
            
            # Ordenar campos
            my_fields.sort(key=lambda x: x["_orden"])
            
            # Quitar _orden del output final clean
            for mf in my_fields:
                if "_orden" in mf: del mf["_orden"]

            config_response[codigo] = {
                "titulo": f.get("TITULO", "Sin Título"),
                "icono": f.get("ICONO", "fa-file"),
                "color": f.get("COLOR", "#333"),
                "campos": my_fields
            }
            
        print("✅ Configuración dinámica servida con éxito.")
        return config_response

    except Exception as e:
        print(f"❌ Error sirviendo config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
async def create_siniestro(request: Request):
    """
    Crea un registro en Airtable mapeando dinámicamente campos y archivos
    basado en la configuración (CONFIG_FORMULARIOS/CAMPOS).
    """
    try:
        # 1. Parsear Multipart Form
        form_data = await request.form()
        
        tipo_formulario = form_data.get("tipo_formulario")
        poliza_record_id = form_data.get("poliza_record_id")
        dni = form_data.get("dni")
        datos_json = form_data.get("datos")
        
        print(f"📝 Recibiendo siniestro Dynamic: {tipo_formulario}")

        if not tipo_formulario or not datos_json:
             raise HTTPException(status_code=400, detail="Faltan datos obligatorios (tipo_formulario, datos)")

        try:
            datos_dict = json.loads(datos_json)
        except:
             raise HTTPException(status_code=400, detail="JSON de datos inválido")

        # 2. Obtener Configuración Dinámica (Mapping)
        # Buscamos el formulario por Slug
        t_forms = get_table("CONFIG_FORMULARIOS")
        params = {"filterByFormula": f"{{CODIGO}}='{tipo_formulario}'", "maxRecords": 1}
        forms_records = t_forms.all(**params)
        
        if not forms_records:
            raise HTTPException(status_code=404, detail=f"Configuración no encontrada para: {tipo_formulario}")
            
        form_record = forms_records[0]
        form_id = form_record["id"]
        
        # Obtenemos los campos de este formulario
        t_campos = get_table("CONFIG_CAMPOS")
        # Filtramos por el Link al Formulario (Esto requiere que 'Formulario' sea un campo Link)
        # Una forma más segura si no sabemos el nombre exacto del campo link:
        # Traer todos y filtrar en memoria (si son pocos) o usar la formula correcta.
        # Asumimos que el campo se llama "Formulario" como en el script.
        # Formula: ver si el ID del form esta en el array de links.
        # SEARCH('recID', ARRAYJOIN({Formulario}))
        
        # Como pyairtable filterByFormula es string:
        filter_formula = f"OR(SEARCH('{form_id}', ARRAYJOIN({{FORMULARIO}})), SEARCH('{form_id}', ARRAYJOIN({{Formulario}})))"
        campos_records = t_campos.all(formula=filter_formula)
        
        # Construir Mapa: ID Frontend -> Columna Airtable
        # { "foto_dni": "FOTO DNI", "fecha": "FECHA DEL SINIESTRO", ... }
        field_map = {}
        file_fields = [] # Lista de IDs que son archivos
        
        for r in campos_records:
            f = r["fields"]
            f_id = f.get("ID CAMPO")
            col = f.get("COLUMNA AIRTABLE")
            f_type = f.get("TIPO")
            
            if f_id and col:
                field_map[f_id] = col
                if f_type == "file":
                    file_fields.append(f_id)

        # 3. Mapear Datos (JSON) -> Airtable Fields
        airtable_payload = {}
        
        # Datos JSON explicitos
        for key, value in datos_dict.items():
            if key in field_map:
                col_name = field_map[key]
                airtable_payload[col_name] = value
                
        # 4. Procesar Archivos
        # Iteramos los keys del form_data que coincidan con campos de archivo
        # Nota: form_data.getlist(key) devuelve lista de UploadFile
        
        # Cache de subidas para no subir 2 veces si el mismo archivo llega por algun motivo (raro)
        
        for f_id in file_fields:
            if f_id in form_data:
                # Puede ser uno o varios archivos (getlist)
                archivos = form_data.getlist(f_id)
                
                urls_adjuntos = [] # Formato para Airtable: [{"url": "..."}]
                
                for archivo in archivos:
                    if isinstance(archivo, UploadFile):
                        print(f"📂 Subiendo archivo para campo {f_id}: {archivo.filename}")
                        link = await upload_file_to_drive(archivo)
                        if link:
                            urls_adjuntos.append({"url": link})
                
                if urls_adjuntos:
                    col_name = field_map[f_id]
                    # Append si ya existe (ej: multi-upload en chunks), pero aqui es todo junto
                    if col_name in airtable_payload:
                        # Si ya habia algo (raro en este flujo), extendemos
                         current = airtable_payload[col_name]
                         if isinstance(current, list):
                             current.extend(urls_adjuntos)
                    else:
                        airtable_payload[col_name] = urls_adjuntos

        # 5. Vinculaciones (Poliza y Cliente) - Mantenemos lógica hardcoded/híbrida
        # porque estos no vienen del config dinamico generalmente, son del contexto
        if poliza_record_id:
            airtable_payload["POLIZAS"] = [poliza_record_id]
            
        if dni:
            dni_limpio = "".join(filter(str.isdigit, str(dni)))
            t_clientes = get_table("CLIENTES")
            if t_clientes and dni_limpio:
                try:
                    c_records = t_clientes.all(formula=f"{{DNI}}='{dni_limpio}'", max_records=1)
                    if c_records:
                        airtable_payload["CLIENTE"] = [c_records[0]["id"]]
                except Exception as e:
                    print(f"Error vinculando cliente: {e}")

        # 6. Guardar en Airtable
        # Estrategia Dinámica: Leer "TABLA RELACIONADA" de la configuración
        # Fallback: Hardcoded por si la config es vieja o incompleta
        
        target_table_name = form_record["fields"].get("TABLA RELACIONADA")

        if not target_table_name:
            # Lógica Legacy (Fallback)
            print("⚠️ Usando Fallback de Tabla (No definido en Config)")
            if tipo_formulario == "accidente":
                target_table_name = "DENUNCIA DE ACCIDENTE"
            elif tipo_formulario == "robo-incendio":
                target_table_name = "DENUNCIA ROBO / INCENDIO"
            elif tipo_formulario == "robo-parcial":
                target_table_name = "DENUNCIA ROBO OC"
            else:
                target_table_name = "DENUNCIAS_GENERICAS" # Ultimo recurso
        
        print(f"Enviando a Airtable {target_table_name}: {json.dumps(airtable_payload, default=str)}") # Log seguro
        
        target_table = get_table(target_table_name)
        record = target_table.create(airtable_payload, typecast=True)
        
        return {"status": "success", "id": record["id"], "message": "Denuncia dinámica creada"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


