import os
import random
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
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
    Replica la lógica de selección inteligente (60% buenos, etc) o simplificada.
    """
    table_calif = get_table("CALIFICACIONES")
    if not table_calif:
        raise HTTPException(status_code=500, detail="Airtable config missing")

    # Fórmula: Visible=True, Autoriza=True, Comentario!=''
    # Y antigüedad < 6 meses (aprox)
    # Airtable formula: AND({VISIBLE}=TRUE(), {AUTORIZA_PUBLICAR}=TRUE(), {COMENTARIO}!='')
    formula = "AND({VISIBLE}=TRUE(), {AUTORIZA_PUBLICAR}=TRUE(), {COMENTARIO}!='')"
    
    # Sort por fecha creación descendente
    records = table_calif.all(formula=formula, sort=["-FECHA DE CREACION"])
    
    if not records:
        return {"testimonios": [], "total": 0, "mensaje": "Sin testimonios disponibles"}

    # Formatear
    formatted = []
    for r in records:
        f = r["fields"]
        nombre = f.get("NOMBRE", "Anónimo")
        estrellas = f.get("ESTRELLAS", 0)
        
        # Iniciales
        partes = nombre.strip().split()
        if partes:
            iniciales = (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper()
        else:
            iniciales = "?"

        # Foto
        foto_url = None
        if f.get("USAR FOTO") and f.get("FOTO PERFIL"):
            fotos = f.get("FOTO PERFIL")
            if isinstance(fotos, list) and len(fotos) > 0:
                foto_url = fotos[0].get("url")

        # Tiempo Relativo (Calculado en Python)
        fecha_creacion = f.get("FECHA DE CREACION") # ISO String endpoint
        texto_tiempo = "Reciente"
        if fecha_creacion:
            try:
                dt = datetime.fromisoformat(fecha_creacion.replace('Z', '+00:00'))
                delta = datetime.now(dt.tzinfo) - dt
                days = delta.days
                if days == 0: texto_tiempo = "Hoy"
                elif days == 1: texto_tiempo = "Ayer"
                elif days < 7: texto_tiempo = f"Hace {days} días"
                elif days < 30: texto_tiempo = f"Hace {days // 7} semanas"
                else: texto_tiempo = f"Hace {days // 30} meses"
            except:
                pass

        formatted.append({
            "id": r["id"],
            "nombre": nombre,
            "iniciales": iniciales,
            "estrellas": estrellas,
            "comentario": f.get("COMENTARIO", ""),
            "fecha": texto_tiempo,
            "fotoUrl": foto_url
        })

    # Lógica de Selección (Shuffle simple y priorizar buenos)
    # Separar por estrellas
    buenos = [t for t in formatted if t["estrellas"] >= 3]
    otros = [t for t in formatted if t["estrellas"] < 3]
    
    random.shuffle(buenos)
    random.shuffle(otros)
    
    # Tomar hasta 7 buenos y 3 otros (Total 10)
    seleccion = buenos[:7] + otros[:3] if len(otros) >= 3 else buenos[:7] + otros
    
    # Completar si falta
    if len(seleccion) < 10:
        restantes_buenos = buenos[7:]
        seleccion.extend(restantes_buenos[:10-len(seleccion)])
    
    random.shuffle(seleccion)

    return {
        "testimonios": seleccion,
        "total": len(seleccion),
        "mensaje": f"Mostrando {len(seleccion)} opiniones"
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
    if data.es_cliente == "Sí" and data.dni:
        fields["DNI"] = data.dni
        if table_clientes:
            # Buscar ID del cliente
            formula = f"{{DNI}}='{data.dni}'"
            c_records = table_clientes.all(formula=formula, max_records=1)
            if c_records:
                fields["CLIENTE"] = [c_records[0]["id"]]  # Link record
                client_linked = True
    
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

@app.post("/api/siniestro")
async def save_siniestro(data: dict = Body(...)):
    """
    Endpoint temporal para Siniestros.
    Por ahora solo loguea, ya que el manejo de archivos requiere storage externo.
    Se recomienda mantener N8N para esto o implementar Cloudinary.
    """
    # TODO: Implementar subida de archivos o conexión a storage.
    print("Siniestro recibido (Python):", data)
    return {
        "status": "success", 
        "message": "Siniestro recibido (sin archivos procesados aún)",
        "data": data
    }
