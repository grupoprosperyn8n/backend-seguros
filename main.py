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

def parse_poliza_block(bloque_texto: str) -> dict:
    """
    Parsea un bloque de ETIQUETA_POLIZA y extrae toda la información.
    
    Ejemplo input:
    "✅ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🔧 AUX"
    
    Returns:
    {
        "numero": "33333333",
        "patente": "PDL384",
        "tipo_vehiculo": "AUTO",
        "categoria": "A",
        "vida": True,
        "auxilio": True,
        "estado": "VENCE 30D",
        "descripcion_completa": "..."
    }
    """
    import re
    
    info = {
        "numero": "",
        "patente": "",
        "tipo_vehiculo": "",
        "categoria": "",
        "vida": False,
        "auxilio": False,
        "estado": "",
        "descripcion_completa": bloque_texto.strip()
    }
    
    # Extraer N° POL
    match = re.search(r'N°\s*POL:\s*(\d+)', bloque_texto)
    if match:
        info["numero"] = match.group(1)
    
    # Extraer Patente
    match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque_texto)
    if match:
        info["patente"] = match.group(1)
    
    # Extraer Tipo de vehículo (después de emoji de vehículo)
    match = re.search(r'[🚗🚙🚛🏍️]\s*([A-Z]+)', bloque_texto)
    if match:
        info["tipo_vehiculo"] = match.group(1)
    
    # Extraer Categoría
    match = re.search(r'🅰️\s*([A-Z])', bloque_texto)
    if match:
        info["categoria"] = match.group(1)
    
    # Extraer VIDA
    info["vida"] = "VIDA: SI" in bloque_texto.upper() or ("❤️" in bloque_texto and "VIDA" in bloque_texto.upper())
    
    # Extraer AUXILIO
    info["auxilio"] = "AUX" in bloque_texto.upper() and "🔧" in bloque_texto
    
    # Extraer Estado (primera parte antes del primer |)
    partes = bloque_texto.split("|")
    if partes:
        estado = partes[0].strip()
        # Limpiar emojis de estado
        for char in ["✅", "⏳", "❌", "⚠️"]:
            estado = estado.replace(char, "")
        info["estado"] = estado.strip()
    
    return info


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
    if isinstance(compilacion, list):
        texto_polizas = " | ".join([str(x) for x in compilacion])
    else:
        texto_polizas = str(compilacion or "")

    patente_upper = patente.upper().strip()
    
    # 3. Verificar si la patente está en el texto de pólizas
    if patente_upper not in texto_polizas.upper():
         return {
            "valid": False,
            "reason": "PATENTE_NOT_FOUND",
            "message": f"Hola {nombre_completo}, no encontramos el vehículo patente {patente_upper} asociado a tu DNI."
        }

    # 4. Verificar estado (ANULADA/BAJA)
    # Buscamos el bloque específico que contiene la patente para ver su estado
    # Formato esperado aprox: "✅ AUTO COROLLA... | ❌ ANULADA AUTO..."
    bloques = texto_polizas.split("|")
    bloque_match = next((b for b in bloques if patente_upper in b.upper()), texto_polizas)
    
    if "ANULADA" in bloque_match.upper() or "BAJA" in bloque_match.upper():
         return {
            "valid": False,
            "reason": "POLICY_INACTIVE",
            "message": f"La póliza del vehículo {patente_upper} figura como ANULADA o DE BAJA."
        }

    # Limpieza de descripción (quitar emojis al inicio si existen)
    # Ej: "✅ ⏳ VENCE 30D AUTO..." -> "AUTO..."
    descripcion = bloque_match.strip()
    # Simple limpieza de caracteres comunes de estado al inicio
    for char in ["✅", "⏳", "❌", "⚠️"]:
        descripcion = descripcion.replace(char, "")
    descripcion = descripcion.strip()

    return {
        "valid": True,
        "message": "Validación exitosa",
        "cliente": {
            "nombres": cliente.get("NOMBRES"),
            "apellido": cliente.get("APELLIDO"),
            "fullname": nombre_completo
        },
        "poliza": {
            "id": "no_disponible_desde_cliente",
            "numero": "0000",
            "patente": patente_upper,
            "descripcion": descripcion
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

    # 4. Verificar estado (ANULADA/BAJA)
    bloques = texto_polizas.split("|")
    bloque_match = next((b for b in bloques if patente_limpia in b.upper()), texto_polizas)
    
    if "ANULADA" in bloque_match.upper() or "BAJA" in bloque_match.upper():
        return {
            "valid": False,
            "message": f"La póliza del vehículo {patente_limpia} figura como ANULADA o DE BAJA."
        }

    # 5. Parsear toda la información de la póliza usando helper
    poliza_info = parse_poliza_block(bloque_match)

    # 6. Retornar datos completos en formato compatible con app.js
    return {
        "valid": True,
        "cliente": {
            "nombres": cliente.get("NOMBRES", ""),
            "apellido": cliente.get("APELLIDO", ""),
        },
        "poliza": {
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


# @app.post("/api/siniestro") -> ENDPOINT REMOVED (Logic moved to Frontend Airtable Param)
