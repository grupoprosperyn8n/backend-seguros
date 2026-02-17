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
    Soporta múltiples pólizas concatenadas separandolas por emojis de estado.
    Retorna una LISTA de diccionarios con la info de cada poliiza encontrada.
    """
    import re
    
    # 1. Limpieza inicial
    if not bloque_texto:
        return []

    # 2. Estrategia de Split: Dividir por emojis de estado que marcan el inicio de un bloque
    SEPARATORS_PATTERN = r'(?=[✅🔴🟢⏳⚠️❌])' 
    
    posibles_bloques = re.split(SEPARATORS_PATTERN, bloque_texto)
    bloques = [b.strip() for b in posibles_bloques if b.strip()]

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
        
        match = re.search(r'N°\s*POL:?\s*(\d+)', bloque, re.IGNORECASE)
        if match:
            p_info["numero"] = match.group(1)
        
        match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque, re.IGNORECASE)
        if match:
            p_info["patente"] = match.group(1).upper()
        
        match = re.search(r'[🚗🚙🚛🏍️]\s+([A-ZÁ-Ú]+)', bloque)
        if match:
            tipo = match.group(1).strip()
            if len(tipo) > 2 and tipo not in ["POL"]: 
                p_info["tipo_vehiculo"] = tipo
            
        if "ANULADA" in bloque:
            p_info["estado"] = "ANULADA"
        elif "VIGENTE" in bloque:
            p_info["estado"] = "VIGENTE"
        
        match_vence = re.search(r'(VENCE\s*\d+D?)', bloque)
        if match_vence:
            p_info["estado"] = match_vence.group(1)
        
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
    
    compilacion = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", [])
    
    texto_polizas = ""
    if isinstance(compilacion, list):
        texto_polizas = " ".join([str(x) for x in compilacion])
    else:
        texto_polizas = str(compilacion or "")

    polizas_encontradas = parse_poliza_block(texto_polizas)
    
    patente_buscada = patente.upper().strip()
    poliza_match = None
    
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

    estado_poliza = poliza_match.get("estado", "").upper()
    if "ANULADA" in estado_poliza or "BAJA" in estado_poliza:
         return {
            "valid": False,
            "reason": "POLICY_INACTIVE",
            "message": f"La póliza del vehículo {patente_buscada} figura como ANULADA o DE BAJA."
        }

    descripcion = poliza_match.get("descripcion_completa", "").strip()
    for char in ["✅", "⏳", "❌", "⚠️"]:
        descripcion = descripcion.replace(char, "")
    descripcion = descripcion.strip()

    record_id_poliza = None
    ids_polizas = cliente.get("POLIZAS", [])
    
    if ids_polizas:
        try:
            table_polizas = get_table("POLIZAS")
            if table_polizas:
                for pid in ids_polizas:
                    try:
                        pol_record = table_polizas.get(pid)
                        fields_p = pol_record["fields"]
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

    formula = "AND({VISIBLE}=TRUE(), {AUTORIZA_PUBLICAR}=TRUE(), {COMENTARIO}!='')"
    
    try:
        records = table_calif.all(formula=formula)
    except Exception as e:
        print(f"Error fetching testimonios: {e}")
        return {"testimonios": [], "total": 0, "mensaje": "Error obteniendo datos"}
    
    if not records:
        return {"testimonios": [], "total": 0, "mensaje": "Sin testimonios disponibles"}

    now = datetime.now().astimezone()
    cutoff_90d = datetime.now().timestamp() - (90 * 24 * 60 * 60)
    
    pool_recent_good = []
    pool_recent_bad = []
    pool_old_good = []
    pool_old_bad = []

    formatted_map = {}

    for r in records:
        f = r["fields"]
        stars = f.get("ESTRELLAS", 0)
        
        date_str = f.get("FECHA DE CREACION") or r.get("createdTime")
        is_recent = False
        
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            is_recent = dt.timestamp() >= cutoff_90d
            
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

        nombre = f.get("NOMBRE", "Anónimo")
        
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
        
        if stars >= 3:
            if is_recent: pool_recent_good.append(item)
            else: pool_old_good.append(item)
        else:
            if is_recent: pool_recent_bad.append(item)
            else: pool_old_bad.append(item)

    random.shuffle(pool_recent_good)
    random.shuffle(pool_recent_bad)
    random.shuffle(pool_old_good)
    random.shuffle(pool_old_bad)

    final_selection = []
    
    target_good = 7
    target_bad = 3
    
    take_bad = pool_recent_bad[:target_bad]
    final_selection.extend(take_bad)
    needed_bad = target_bad - len(take_bad)
    
    if needed_bad > 0:
        take_bad_old = pool_old_bad[:needed_bad]
        final_selection.extend(take_bad_old)
        
    take_good = pool_recent_good[:target_good]
    final_selection.extend(take_good)
    needed_good = target_good - len(take_good)
    
    if needed_good > 0:
        take_good_old = pool_old_good[:needed_good]
        final_selection.extend(take_good_old)
        
    current_ids = {x["id"] for x in final_selection}
    leftovers = []
    
    for pool in [pool_recent_good, pool_old_good, pool_recent_bad, pool_old_bad]:
        for item in pool:
            if item["id"] not in current_ids:
                leftovers.append(item)
                
    random.shuffle(leftovers)
    needed_total = 10 - len(final_selection)
    if needed_total > 0:
        final_selection.extend(leftovers[:needed_total])

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
        "EMPLEADO": ["recrUCS6NhFjVmzqm"]
    }

    client_linked = False
    
    if data.es_cliente == "Sí" and data.dni:
        fields["ES_CLIENTE"] = "No" 
        
        dni_limpio = "".join(filter(str.isdigit, str(data.dni)))

        if table_clientes and dni_limpio:
            try:
                formula = f"{{DNI}}={dni_limpio}"
                c_records = table_clientes.all(formula=formula, max_records=1)
                
                if c_records:
                    fields["CLIENTE"] = [c_records[0]["id"]]
                    fields["ES_CLIENTE"] = "Sí"
                    fields["DNI"] = int(dni_limpio)
                    client_linked = True
                else:
                    pass
            except Exception as e_airtable:
                print(f"Error buscando cliente en Airtable: {e_airtable}")
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

    # 4. Extraer el bloque completo de la póliza
    parts = [p.strip() for p in texto_polizas.split("|")]
    bloques_detectados = []
    current_bloque = []
    
    emojis_inicio = ["✅", "❌", "⏳", "⚠️"]
    
    for part in parts:
        es_inicio = any(e in part for e in emojis_inicio) and ("VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part)
        
        if not current_bloque:
            current_bloque.append(part)
        elif es_inicio:
            bloques_detectados.append(" | ".join(current_bloque))
            current_bloque = [part]
        else:
            current_bloque.append(part)
            
    if current_bloque:
        bloques_detectados.append(" | ".join(current_bloque))
        
    bloque_match = None
    for bloque in bloques_detectados:
        if patente_limpia in bloque.upper():
            bloque_match = bloque
            break
            
    if not bloque_match:
        bloque_match = texto_polizas

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
    record_id_poliza = None
    ids_polizas = cliente.get("POLIZAS", [])
    
    if ids_polizas:
        try:
            table_polizas = get_table("POLIZAS")
            if table_polizas:
                for pid in ids_polizas:
                    try:
                        pol_record = table_polizas.get(pid)
                        fields_p = pol_record["fields"]
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
            "record_id": record_id_poliza,
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
        
        # 2. Traer Todos los Campos
        campos_records = t_campos.all()
        
        config_response = {}
        
        for f_rec in forms_records:
            f = f_rec["fields"]
            codigo = f.get("CODIGO")
            visible = f.get("VISIBILIDAD", False)
            
            if not codigo or not visible: continue
            
            form_id = f_rec["id"]
            
            my_fields = []
            for c_rec in campos_records:
                c = c_rec["fields"]
                linked_forms = c.get("FORMULARIO") or c.get("Formulario", [])
                if form_id in linked_forms:
                    campo_front = {
                        "id": c.get("ID CAMPO"),
                        "label": c.get("ETIQUETA"),
                        "type": c.get("TIPO", "text"),
                        "required": c.get("OBLIGATORIO", False),
                        "placeholder": c.get("PLACEHOLDER", ""),
                        "options": c.get("OPCIONES", "").split(",") if c.get("OPCIONES") else [],
                    }
                    # NO exponer COLUMNA AIRTABLE al frontend (info interna)
                    campo_front = {k: v for k, v in campo_front.items() if v is not None}
                    
                    campo_front["_orden"] = c.get("ORDEN", 999)
                    
                    my_fields.append(campo_front)
            
            my_fields.sort(key=lambda x: x["_orden"])
            
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
# CREACIÓN DE SINIESTRO
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
        t_forms = get_table("CONFIG_FORMULARIOS")
        params = {"filterByFormula": f"{{CODIGO}}='{tipo_formulario}'", "maxRecords": 1}
        forms_records = t_forms.all(**params)
        
        if not forms_records:
            raise HTTPException(status_code=404, detail=f"Configuración no encontrada para: {tipo_formulario}")
            
        form_record = forms_records[0]
        form_id = form_record["id"]
        
        # Obtenemos los campos de este formulario
        t_campos = get_table("CONFIG_CAMPOS")
        filter_formula = f"OR(SEARCH('{form_id}', ARRAYJOIN({{FORMULARIO}})), SEARCH('{form_id}', ARRAYJOIN({{Formulario}})))"
        campos_records = t_campos.all(formula=filter_formula)
        
        # Construir Mapa: ID Frontend -> Columna Airtable
        field_map = {}
        file_fields = []
        
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
        
        for key, value in datos_dict.items():
            if key in field_map:
                col_name = field_map[key]
                airtable_payload[col_name] = value
                
        # 4. Procesar Archivos
        for f_id in file_fields:
            if f_id in form_data:
                archivos = form_data.getlist(f_id)
                
                urls_adjuntos = []
                
                for archivo in archivos:
                    if isinstance(archivo, UploadFile):
                        print(f"📂 Subiendo archivo para campo {f_id}: {archivo.filename}")
                        link = await upload_file_to_drive(archivo)
                        if link:
                            urls_adjuntos.append({"url": link})
                
                if urls_adjuntos:
                    col_name = field_map[f_id]
                    if col_name in airtable_payload:
                         current = airtable_payload[col_name]
                         if isinstance(current, list):
                             current.extend(urls_adjuntos)
                    else:
                        airtable_payload[col_name] = urls_adjuntos

        # 5. Vinculaciones (Poliza y Cliente)
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
        target_table_name = form_record["fields"].get("TABLA RELACIONADA")

        if not target_table_name:
            print("⚠️ Usando Fallback de Tabla (No definido en Config)")
            if tipo_formulario == "accidente":
                target_table_name = "DENUNCIA DE ACCIDENTE"
            elif tipo_formulario == "robo-incendio":
                target_table_name = "DENUNCIA ROBO / INCENDIO"
            elif tipo_formulario == "robo-parcial":
                target_table_name = "DENUNCIA ROBO OC"
            else:
                target_table_name = "DENUNCIAS_GENERICAS"
        
        print(f"Enviando a Airtable {target_table_name}: {json.dumps(airtable_payload, default=str)}")
        
        target_table = get_table(target_table_name)
        record = target_table.create(airtable_payload, typecast=True)
        
        return {"status": "success", "id": record["id"], "message": "Denuncia dinámica creada"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


