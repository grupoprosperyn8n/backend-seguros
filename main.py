from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyairtable import Table
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Airtable Config
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def get_table(table_name: str):
    return Table(API_KEY, BASE_ID, table_name)

# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class SiniestroRequest(BaseModel):
    dni: str
    patente: str
    tipo: str
    descripcion: str
    fecha: str
    hora: str
    ubicacion: str
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
    
    # Extraer N° POL (buscar patrón más flexible)
    match = re.search(r'N°\s*POL:?\s*(\d+)', bloque_texto, re.IGNORECASE)
    if match:
        info["numero"] = match.group(1)
    
    # Extraer Patente (después del emoji 🏷️)
    match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque_texto)
    if match:
        info["patente"] = match.group(1)
    
    # Extraer Tipo de vehículo (buscar palabra después de emoji de vehículo)
    # Formato: "🚗 AUTO" o "🚛 CAMIONETA"
    match = re.search(r'[🚗🚙🚛🏍️]\s+([A-ZÁ-Ú]+)', bloque_texto)
    if match:
        tipo = match.group(1).strip()
        # Filtrar palabras que no son tipos de vehículo
        if tipo not in ['VENCE', 'POL', 'VIDA', 'AUX', 'ANULADA', 'BAJA']:
            info["tipo_vehiculo"] = tipo
    
    # Extraer Categoría (después del emoji 🅰️)
    match = re.search(r'🅰️\s*([A-Z])', bloque_texto)
    if match:
        info["categoria"] = match.group(1)
    
    # Extraer VIDA (buscar "VIDA: SI" o solo emoji ❤️)
    if re.search(r'VIDA:\s*SI', bloque_texto, re.IGNORECASE):
        info["vida"] = True
    elif '❤️' in bloque_texto and 'VIDA' not in bloque_texto.upper():
        # Si tiene el emoji pero no dice explícitamente, asumir SI
        info["vida"] = True
    
    # Extraer AUXILIO (buscar "AUX" con emoji 🔧)
    if '🔧' in bloque_texto and 'AUX' in bloque_texto.upper():
        info["auxilio"] = True
    
    # Extraer Estado (primera parte antes del primer | que no sea emoji)
    partes = bloque_texto.split("|")
    if partes:
        estado = partes[0].strip()
        # Limpiar emojis de estado
        for char in ["✅", "⏳", "❌", "⚠️"]:
            estado = estado.replace(char, "")
        estado = estado.strip()
        # Validar que no sea solo un emoji o vacío
        if estado and len(estado) > 2:
            info["estado"] = estado
    
    return info


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/")
def read_root():
    return {"status": "Backend Seguros OK"}

# ==============================================================================
# LOGIN
# ==============================================================================

@app.post("/api/login")
def login(request: LoginRequest):
    table = get_table("USUARIOS")
    formula = f'AND({{EMAIL}}="{request.email}", {{PASSWORD}}="{request.password}")'
    records = table.all(formula=formula, max_records=1)
    
    if not records:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    user = records[0]["fields"]
    estado = user.get("ESTADO", "").upper()
    
    if estado != "ACTIVO":
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    
    return {
        "success": True,
        "user": {
            "email": user.get("EMAIL"),
            "rol": user.get("ROL"),
            "estado": user.get("ESTADO")
        }
    }

# ==============================================================================
# PORTAL CONTENT
# ==============================================================================

@app.get("/api/portal")
def get_portal_content(rol: str):
    table = get_table("PORTAL CONTENIDO")
    formula = f'{{ROL}}="{rol}"'
    records = table.all(formula=formula, max_records=1)
    
    if not records:
        return {"frase": "Bienvenido", "imagen": ""}
    
    content = records[0]["fields"]
    return {
        "frase": content.get("FRASE", "Bienvenido"),
        "imagen": content.get("IMAGEN", [""])[0] if content.get("IMAGEN") else ""
    }

# ==============================================================================
# REGISTRO
# ==============================================================================

@app.post("/api/register")
def register(request: LoginRequest):
    table = get_table("USUARIOS")
    
    # Verificar si ya existe
    formula = f'{{EMAIL}}="{request.email}"'
    existing = table.all(formula=formula, max_records=1)
    
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear nuevo usuario
    table.create({
        "EMAIL": request.email,
        "PASSWORD": request.password,
        "ESTADO": "Pendiente",
        "ROL": "Empleado"
    })
    
    return {"success": True, "message": "Usuario registrado exitosamente"}

# ==============================================================================
# VALIDAR CLIENTE (DENUNCIAS)
# ==============================================================================

@app.get("/api/validar-cliente")
def validar_cliente(dni: str):
    """
    Valida si un cliente existe en Airtable y retorna sus pólizas activas.
    """
    table_clientes = get_table("CLIENTES")
    
    # Buscar cliente por DNI
    formula = f'({{DNI}} & "") = "{dni}"'
    records = table_clientes.all(formula=formula, max_records=1)
    
    if not records:
        return {
            "valid": False,
            "message": "No encontramos un cliente con ese DNI."
        }
    
    cliente = records[0]["fields"]
    
    # Obtener pólizas compiladas
    polizas_texto = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", "")
    
    if not polizas_texto or polizas_texto.strip() == "":
        return {
            "valid": False,
            "message": "No encontramos pólizas activas asociadas a tu DNI."
        }
    
    # Verificar si todas las pólizas están anuladas o de baja
    if all(keyword in polizas_texto.upper() for keyword in ["ANULADA", "BAJA"]):
        return {
            "valid": False,
            "message": "Tus pólizas figuran como ANULADAS o DE BAJA."
        }
    
    return {
        "valid": True,
        "cliente": {
            "nombres": cliente.get("NOMBRES", ""),
            "apellido": cliente.get("APELLIDO", ""),
            "polizas": polizas_texto
        }
    }

# ==============================================================================
# VALIDAR SINIESTRO (CLIENTE + PATENTE)
# ==============================================================================

@app.get("/api/validate-siniestro")
def validate_siniestro(dni: str, patente: str):
    """
    Valida DNI + Patente para reportar siniestro.
    Retorna información completa de la póliza parseada.
    """
    table_clientes = get_table("CLIENTES")
    
    # 1. Buscar cliente por DNI
    formula = f'({{DNI}} & "") = "{dni}"'
    records = table_clientes.all(formula=formula, max_records=1)
    
    if not records:
        return {
            "valid": False,
            "message": "No encontramos un cliente con ese DNI."
        }
    
    cliente = records[0]["fields"]
    
    # 2. Obtener texto de pólizas compiladas
    texto_polizas = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", "")
    
    if not texto_polizas or texto_polizas.strip() == "":
        return {
            "valid": False,
            "message": "No encontramos pólizas asociadas a tu DNI."
        }
    
    # 3. Verificar si la patente está en el texto de pólizas
    patente_limpia = patente.strip().upper()
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
