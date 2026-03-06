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
import httpx


load_dotenv()

app = FastAPI()
# Force Deploy v2

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://seguros_linktree.surge.sh",
        "https://seguros-app-linktree.surge.sh",
        "https://login-agentico-1770227340.surge.sh",
        "https://registro-agentico-1770227370.surge.sh",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Configuración Airtable
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not API_KEY or not BASE_ID:
    print("WARNING: AIRTABLE_API_KEY or AIRTABLE_BASE_ID not set")

# Mapeo de nombres de tablas a IDs para Content API
TABLE_NAME_TO_ID = {
    "DENUNCIA DE ACCIDENTE": "tbl4570W1T0qGdj8w",
    "DENUNCIA ROBO OC": "tblRsZQhnNdJqnxf8",
    "DENUNCIA ROBO / INCENDIO": "tblLnVFRONjVZ7YUH",
    "GESTIÓN GENERAL": "tblF8sSjgj8J9kLm",
    "CLIENTES": "tblVAcMxNTLYXbLfT",
    "POLIZAS": "tblXZcdefgh123456",
    "CALIFICACIONES": "tblAbcdefgh12345",
}

# ==============================================================================
# CONSTANTES DE ESTADO WEB
# ==============================================================================


class EstadoWeb:
    """
    Valores para el campo ESTADO_WEB en tablas de denuncias (Single Select).

    IMPORTANTE: Single Select requiere match EXACTO con las opciones en Airtable.
    Debido a posibles diferencias de rendering (con/sin espacio después del emoji),
    se proveen ambos formatos con fallback automático.

    Tablas que usan este campo:
    - DENUNCIA DE ACCIDENTE
    - DENUNCIA ROBO OC
    - DENUNCIA ROBO / INCENDIO

    Verificado: 2026-03-03
    - Meta API retorna: "🆕 NUEVO WEB" (con espacio U+0020)
    - Registros poblados usan: "🆕 NUEVO WEB" (con espacio)
    - Pero UI puede verse sin espacio (rendering)
    """

    # Formato principal (con espacio - según datos técnicos)
    NUEVO_WEB_CON_ESPACIO = "🆕 NUEVO WEB"
    VISTO_CON_ESPACIO = "👀 VISTO"
    PROCESADO_CON_ESPACIO = "✅ PROCESADO"

    # Formato alternativo (sin espacio - por si UI es diferente)
    NUEVO_WEB_SIN_ESPACIO = "🆕NUEVO WEB"
    VISTO_SIN_ESPACIO = "👀VISTO"
    PROCESADO_SIN_ESPACIO = "✅PROCESADO"

    # Formato a usar (CAMBIAR AQUÍ si el principal no funciona)
    # True = con espacio | False = sin espacio
    USAR_CON_ESPACIO = True

    @classmethod
    def nuevo_web(cls):
        """Retorna el valor correcto para ESTADO_WEB = NUEVO"""
        return (
            cls.NUEVO_WEB_CON_ESPACIO
            if cls.USAR_CON_ESPACIO
            else cls.NUEVO_WEB_SIN_ESPACIO
        )

    @classmethod
    def visto(cls):
        """Retorna el valor correcto para ESTADO_WEB = VISTO"""
        return cls.VISTO_CON_ESPACIO if cls.USAR_CON_ESPACIO else cls.VISTO_SIN_ESPACIO

    @classmethod
    def procesado(cls):
        """Retorna el valor correcto para ESTADO_WEB = PROCESADO"""
        return (
            cls.PROCESADO_CON_ESPACIO
            if cls.USAR_CON_ESPACIO
            else cls.PROCESADO_SIN_ESPACIO
        )


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
    keywords_inicio = [
        "VIGENTE",
        "VENCE",
        "ANULADA",
        "BAJA",
        "ACTIVA",
        "SIN VIGENCIA",
        "SIN POLIZAS",
        "TRAMITES",
    ]

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
            "descripcion_completa": bloque,
        }

        # Extraer N POL — usar [0-9] en vez de d, [ ] en vez de s
        match = re.search(r"N[°][ ]*POL[:]?[ ]*([0-9]+)", bloque, re.IGNORECASE)
        if not match:
            # Fallback: buscar cualquier secuencia de 5+ digitos como numero de poliza pero evitar patentes numericas largas (raro)
            match = re.search(r"([0-9]{5,})", bloque)
        if match:
            p_info["numero"] = match.group(1)

        # Extraer Patente con emoji
        # Intentamos capturar lo que sigue al emoji de etiqueta
        match = re.search(
            r"🏷️?[ ]*([A-Z]{2,3}[0-9]{3}[A-Z]{0,2}|[A-Z0-9]{6,9})", bloque, re.IGNORECASE
        )
        # Refinamiento: Si hay un emoji "🏷️" explícito, tomamos lo que sigue
        match_explicit = re.search(r"🏷️[ ]*([A-Z0-9]+)", bloque, re.IGNORECASE)

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
        match = re.search(r"[🚗🚙🚛🏍️][ ]+([A-ZÁ-Ú]+)", bloque)
        if match:
            tipo = match.group(1).strip()
            if len(tipo) > 2 and tipo not in ["POL"]:
                p_info["tipo_vehiculo"] = tipo

        # Si no encontro tipo, buscar palabras clave comunes
        if not p_info["tipo_vehiculo"]:
            for tipo_clave in [
                "AUTOMOVIL",
                "AUTO",
                "CAMIONETA",
                "MOTO",
                "CAMION",
                "UTILITARIO",
                "PICK UP",
                "PICKUP",
            ]:
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

        match_vence = re.search(r"(VENCE[ ]*[0-9]+[D]?)", bloque_upper)
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
    formula = f'({{DNI}} & "") = "{dni}"'
    try:
        records = table_clientes.all(formula=formula, max_records=1)
    except Exception as e:
        print(f"Error Airtable: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to database")

    if not records:
        return {
            "valid": False,
            "reason": "CLIENT_NOT_FOUND",
            "message": f"No encontramos un cliente con el DNI ingresado ({dni}). Verificá que esté escrito correctamente.",
        }

    cliente = records[0]["fields"]
    nombre_completo = (
        cliente.get("NOMBRE COMPLETO") or cliente.get("NOMBRES") or "Cliente"
    )

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
            "message": f"Hola {nombre_completo}, no encontramos el vehículo patente {patente_buscada} asociado a tu DNI.",
        }

    # 4. Verificar estado (ANULADA/BAJA)
    estado_poliza = poliza_match.get("estado", "").upper()
    if "ANULADA" in estado_poliza or "BAJA" in estado_poliza:
        return {
            "valid": False,
            "reason": "POLICY_INACTIVE",
            "message": f"La póliza del vehículo {patente_buscada} figura como ANULADA o DE BAJA.",
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
                    except Exception as e:
                        print(f"Error parseando póliza {pid}: {e}")
                        continue
        except Exception as e:
            print(f"Error fetching poliza details: {e}")

    return {
        "valid": True,
        "message": "Validación exitosa",
        "cliente": {
            "nombres": cliente.get("NOMBRES"),
            "apellido": cliente.get("APELLIDO"),
            "fullname": nombre_completo,
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
            "descripcion_completa": descripcion,
        },
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
    now = datetime.now().astimezone()  # Aware
    cutoff_90d = datetime.now().timestamp() - (
        90 * 24 * 60 * 60
    )  # Timestamp comparison logic easier

    pool_recent_good = []
    pool_recent_bad = []
    pool_old_good = []
    pool_old_bad = []

    formatted_map = {}  # ID -> Formatted Dict

    for r in records:
        f = r["fields"]
        stars = f.get("ESTRELLAS", 0)

        # Parse Date
        date_str = f.get("FECHA DE CREACION") or r.get("createdTime")
        is_recent = False

        # Intentar parsear fecha
        try:
            # ISO format from Airtable: 2023-10-25T12:00:00.000Z
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            is_recent = dt.timestamp() >= cutoff_90d

            # Texto relativo
            delta = datetime.now(dt.tzinfo) - dt
            days = delta.days
            if days == 0:
                texto_tiempo = "Hoy"
            elif days == 1:
                texto_tiempo = "Ayer"
            elif days < 7:
                texto_tiempo = f"Hace {days} días"
            elif days < 30:
                texto_tiempo = f"Hace {days // 7} semanas"
            else:
                texto_tiempo = f"Hace {days // 30} meses"
        except Exception as e:
            print(f"Error calculando tiempo relativo de siniestro {date_str}: {e}")
            texto_tiempo = "Reciente"
            is_recent = False

        # Formatear
        nombre = f.get("NOMBRE", "Anónimo")

        # Iniciales
        partes = nombre.strip().split()
        if partes:
            iniciales = (
                partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")
            ).upper()
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
            "fotoUrl": foto_url,
        }

        formatted_map[r["id"]] = item

        # Clasificar
        if stars >= 3:
            if is_recent:
                pool_recent_good.append(item)
            else:
                pool_old_good.append(item)
        else:
            if is_recent:
                pool_recent_bad.append(item)
            else:
                pool_old_bad.append(item)

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
        "mensaje": f"Mostrando {len(final_selection)} opiniones",
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
    except Exception as e:
        print(f"Error obteniendo calificaciones: {e}")
        return {"rating": 0, "total": 0}

    if not records:
        return {"rating": 0, "total": 0}

    total_stars = sum(r["fields"].get("ESTRELLAS", 0) for r in records)
    count = len(records)
    if count == 0:
        return {"rating": 0, "total": 0}

    average = round(total_stars / count, 1)

    return {"rating": average, "total": count}


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
        "EMPLEADO": ["recrUCS6NhFjVmzqm"],  # ID Agente Online
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
                    fields["DNI"] = int(
                        dni_limpio
                    )  # Guardar como número si el campo destino lo permite o string limpio
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
            "clienteVinculado": client_linked,
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
    formula = f'({{DNI}} & "") = "{dni_limpio}"'
    try:
        records = table_clientes.all(formula=formula, max_records=1)
    except Exception as e:
        print(f"Error buscando cliente: {e}")
        return {"valid": False, "message": "Error validando cliente"}

    if not records:
        return {"valid": False, "message": "Cliente no encontrado"}

    cliente = records[0]["fields"]
    nombre_completo = (
        cliente.get("NOMBRE COMPLETO") or cliente.get("NOMBRES") or "Cliente"
    )

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
            "message": f"No encontramos el vehículo patente {patente_limpia} asociado a tu DNI.",
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
        es_inicio = any(e in part for e in emojis_inicio) and (
            "VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part
        )

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
            "message": f"La póliza del vehículo {patente_limpia} figura como ANULADA o DE BAJA.",
        }

    # 5. Parsear toda la información de la póliza usando helper
    parsed_list = parse_poliza_block(bloque_match)
    # parse_poliza_block retorna una LISTA — tomar el primer elemento
    poliza_info = (
        parsed_list[0]
        if parsed_list
        else {
            "numero": "",
            "patente": patente_limpia,
            "tipo_vehiculo": "",
            "categoria": "",
            "vida": False,
            "auxilio": False,
            "estado": "CONSULTAR",
            "descripcion_completa": bloque_match,
        }
    )

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
                    except Exception as e:
                        print(f"Error al analizar póliza con patente_limpia: {e}")
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
            "record_id": record_id_poliza,  # ID para Linked Record
            "numero": poliza_info["numero"],
            "patente": poliza_info["patente"],
            "tipo_vehiculo": poliza_info["tipo_vehiculo"],
            "categoria": poliza_info["categoria"],
            "vida": poliza_info["vida"],
            "auxilio": poliza_info["auxilio"],
            "estado": poliza_info["estado"],
            "descripcion_completa": poliza_info["descripcion_completa"],
        },
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

            if not codigo or not visible:
                continue

            form_id = f_rec["id"]
            form_id_str = str(form_id)

            # Filtrar campos para este formulario
            # El campo "Formulario" en CONFIG_CAMPOS es un array de IDs [RecID]
            my_fields = []
            for c_rec in campos_records:
                c = c_rec["fields"]
                linked_forms = c.get("FORMULARIO") or c.get("Formulario", [])
                # Convertir a strings para comparación robusta
                linked_forms_str = [str(fid) for fid in linked_forms]
                if form_id_str in linked_forms_str:
                    # Mapear a estructura Frontend
                    campo_front = {
                        "id": c.get("ID CAMPO"),
                        "label": c.get("ETIQUETA"),
                        "type": c.get("TIPO", "text"),
                        "required": c.get("OBLIGATORIO", False),
                        # Opcionales
                        "placeholder": c.get("PLACEHOLDER", ""),
                        "options": c.get("OPCIONES", "").split(",")
                        if c.get("OPCIONES")
                        else [],
                    }
                    # NO exponer COLUMNA AIRTABLE al frontend (info interna)
                    # Limpieza de None
                    campo_front = {
                        k: v for k, v in campo_front.items() if v is not None
                    }

                    # Agregar orden si existe para sortear despues
                    campo_front["_orden"] = c.get("ORDEN", 999)

                    my_fields.append(campo_front)

            # Ordenar campos
            my_fields.sort(key=lambda x: x["_orden"])

            # Quitar _orden del output final clean
            for mf in my_fields:
                if "_orden" in mf:
                    del mf["_orden"]

            config_response[codigo] = {
                "titulo": f.get("TITULO", "Sin Título"),
                "icono": f.get("ICONO", "fa-file"),
                "color": f.get("COLOR", "#333"),
                "campos": my_fields,
            }

        print("✅ Configuración dinámica servida con éxito.")
        return config_response

    except Exception as e:
        print(f"❌ Error sirviendo config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# CREACIÓN DE SINIESTRO (Python Puro — Sin n8n)
# ==============================================================================


def _generar_id_gestion(tabla_destino: str) -> str:
    """
    Genera un ID de gestión único para un siniestro.
    Formato: SIN-2026-0001 (año + secuencial por tabla)
    """
    now = datetime.now()
    year = now.strftime("%Y")

    # Intentar obtener el último ID de la tabla para continuar la secuencia
    try:
        t = get_table(tabla_destino)
        if t:
            # Buscar registros con ID_GESTION_UNICO que empiece con SIN-{year}
            records = t.all(
                formula=f"SEARCH('SIN-{year}', {{ID_GESTION_UNICO}})",
                fields=["ID_GESTION_UNICO"],
                sort=["ID_GESTION_UNICO"],
            )
            if records:
                # Extraer el número más alto
                max_num = 0
                for r in records:
                    gid = r["fields"].get("ID_GESTION_UNICO", "")
                    try:
                        num = int(gid.split("-")[-1])
                        if num > max_num:
                            max_num = num
                    except Exception as e:
                        print(f"Error parseando numero de gestión secuencial: {e}")
                        continue
                return f"SIN-{year}-{str(max_num + 1).zfill(4)}"
    except Exception as e:
        print(f"⚠️ Error generando ID secuencial: {e}")

    # Fallback: timestamp único
    ts = now.strftime("%m%d%H%M")
    return f"SIN-{year}-{ts}"


@app.post("/api/create-siniestro")
async def create_siniestro(request: Request):
    """
    Crea un registro de siniestro directamente en Airtable.
    Flujo: Parsea datos → Sube archivos a Drive → Lee config dinámica → Mapea campos → Escribe en Airtable.
    100% Python, sin dependencia de n8n.
    """
    try:
        # ==================================================================
        # 1. PARSEAR FORMDATA
        # ==================================================================
        form_data = await request.form()
        tipo_formulario = form_data.get("tipo_formulario")
        poliza_record_id = form_data.get("poliza_record_id")
        dni = form_data.get("dni")
        datos_json = form_data.get("datos")

        print(f"📝 create_siniestro v4 (Python puro): {tipo_formulario}")

        if not tipo_formulario or not datos_json:
            raise HTTPException(
                status_code=400,
                detail="Datos incompletos: falta tipo_formulario o datos",
            )

        try:
            datos_dict = json.loads(datos_json)
        except Exception as e:
            print(f"Error parseando JSON de siniestro: {e}")
            raise HTTPException(status_code=400, detail="JSON de datos inválido")

        # ==================================================================
        # 3. LEER CONFIGURACIÓN DINÁMICA DE AIRTABLE
        # ==================================================================
        t_forms = get_table("CONFIG_FORMULARIOS")
        t_campos = get_table("CONFIG_CAMPOS")

        if not t_forms or not t_campos:
            raise HTTPException(
                status_code=500,
                detail="Error de configuración: tablas CONFIG no disponibles",
            )

        # Buscar el formulario por CODIGO
        forms_records = t_forms.all()
        form_record = None
        for f_rec in forms_records:
            if f_rec["fields"].get("CODIGO") == tipo_formulario:
                form_record = f_rec
                break

        if not form_record:
            raise HTTPException(
                status_code=400,
                detail=f"Formulario '{tipo_formulario}' no encontrado en CONFIG_FORMULARIOS",
            )

        form_id = form_record["id"]
        tabla_destino = form_record["fields"].get("TABLA RELACIONADA")

        if not tabla_destino:
            raise HTTPException(
                status_code=500,
                detail=f"Formulario '{tipo_formulario}' no tiene TABLA RELACIONADA configurada",
            )

        print(f"   📋 Formulario: {tipo_formulario} → Tabla: {tabla_destino}")

        # ==================================================================
        # 4. MAPEAR DATOS DEL FORMULARIO A COLUMNAS AIRTABLE
        # ==================================================================
        # Construir mapa: id_campo_frontend → columna_airtable
        field_map = {}
        campos_records = t_campos.all()

        print(f"   🔍 DEBUG: form_id='{form_id}' (type: {type(form_id)})")

        for c_rec in campos_records:
            c = c_rec["fields"]
            linked_forms = c.get("FORMULARIO") or c.get("Formulario", [])
            # Debug: asegurar que form_id sea string para comparación
            form_id_str = str(form_id) if form_id else ""
            linked_forms_str = [str(fid) for fid in linked_forms]

            print(
                f"   🔍 DEBUG: Campo '{c.get('ID CAMPO')}' - linked_forms: {linked_forms_str}"
            )

            if form_id_str in linked_forms_str:
                id_campo = c.get("ID CAMPO")
                columna = c.get("COLUMNA AIRTABLE")
                print(f"   🔍 DEBUG: MATCH! '{id_campo}' -> '{columna}'")
                if id_campo and columna:
                    field_map[id_campo] = columna

        print(f"   🗺️ Campos mapeados: {field_map}")

        # Recolectar archivos para subir después (Airtable Content API requiere Record ID)
        archivos_para_subir = {}  # { columna_airtable: [UploadFile] }
        archivos_fallidos = []

        # Debug: mostrar todas las keys recibidas en form_data
        print(f"   🔍 DEBUG: Keys en form_data: {list(form_data.keys())}")

        # Recolectar archivos - manejar múltiples archivos por campo
        for key in form_data.keys():
            # Usar getlist para obtener todos los valores (incluyendo múltiples archivos)
            items = form_data.getlist(key)

            print(
                f"   🔍 DEBUG: key='{key}', items count={len(items)}, types={[type(i).__name__ for i in items]}"
            )

            for item in items:
                # Verificar si es un archivo de manera más robusta
                # FastAPI puede devolver UploadFile o puede haber sido leído
                es_archivo = False
                nombre_archivo = ""

                if hasattr(item, "filename") and item.filename:
                    es_archivo = True
                    nombre_archivo = item.filename
                elif isinstance(item, str) and key in field_map:
                    # Si es string, no es archivo
                    es_archivo = False

                print(
                    f"   🔍 DEBUG: item es archivo: {es_archivo}, filename: {nombre_archivo}"
                )

                if es_archivo and nombre_archivo:
                    # Encontrar el nombre de columna en Airtable para este campo
                    columna = field_map.get(key)
                    print(f"   🔍 DEBUG: Mapeo encontrado: '{key}' -> '{columna}'")
                    if columna:
                        if columna not in archivos_para_subir:
                            archivos_para_subir[columna] = []
                        archivos_para_subir[columna].append(item)
                        print(
                            f"📂 Recolectado para subir: {key} ({nombre_archivo}) -> {columna}"
                        )
                    else:
                        print(
                            f"⚠️ Campo de archivo '{key}' no mapeado en CONFIG_CAMPOS. Field map: {field_map}"
                        )

        # Construir payload para Airtable
        airtable_payload = {}

        # 4a. Mapear datos de texto/selects/etc.
        for campo_id, valor in datos_dict.items():
            if campo_id in field_map and valor not in (None, "", []):
                airtable_payload[field_map[campo_id]] = valor

        # 4c. Vincular póliza
        if poliza_record_id:
            airtable_payload["POLIZAS"] = [poliza_record_id]

        # ==================================================================
        # 5. BUSCAR CLIENTE POR DNI Y VINCULAR
        # ==================================================================
        if dni:
            try:
                t_clientes = get_table("CLIENTES")
                if t_clientes:
                    dni_limpio = "".join(filter(str.isdigit, str(dni)))
                    formula = f'({{DNI}} & "") = "{dni_limpio}"'
                    cliente_records = t_clientes.all(formula=formula, max_records=1)
                    if cliente_records:
                        airtable_payload["CLIENTE"] = [cliente_records[0]["id"]]
                        print(f"   👤 Cliente vinculado: {cliente_records[0]['id']}")
            except Exception as e:
                print(f"   ⚠️ Error buscando cliente: {e}")

        # ==================================================================
        # 6. AGREGAR CAMPOS AUTOMÁTICOS
        # ==================================================================

        # ID de gestión único ya NO se genera acá porque es un campo FÓRMULA en Airtable
        # Airtable lo genera automáticamente basándose en otros campos vinculados

        # Estado web - Usa valor con fallback automático
        estado_web_valor = EstadoWeb.nuevo_web()
        airtable_payload["ESTADO_WEB"] = estado_web_valor
        print(
            f"   🏷️  ESTADO_WEB configurado: '{estado_web_valor}' (formato: {'CON espacio' if EstadoWeb.USAR_CON_ESPACIO else 'SIN espacio'})"
        )

        print(f"   📦 Payload Airtable keys: {list(airtable_payload.keys())}")

        # ==================================================================
        # 7. CREAR REGISTRO EN AIRTABLE
        # ==================================================================
        t_destino = get_table(tabla_destino)
        if not t_destino:
            raise HTTPException(
                status_code=500,
                detail=f"No se pudo conectar a la tabla '{tabla_destino}'",
            )

        try:
            # typecast=True para que Airtable convierta tipos automáticamente
            # (ej: string "14" → number 14 si el campo es Number)
            record = t_destino.create(airtable_payload, typecast=True)
            record_id = record.get("id", "N/A")

            # Obtener el ID de gestión generado por Airtable (fórmula)
            id_gestion = record.get("fields", {}).get("ID_GESTION_UNICO", record_id)
            print(f"✅ Siniestro creado exitosamente: {record_id} ({id_gestion})")

            # ==================================================================
            # 8. SUBIR ARCHIVOS VIA AIRTABLE CONTENT API
            # ==================================================================
            print(f"   🔍 DEBUG: Archivos a subir: {archivos_para_subir}")

            # https://content.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}/{fieldIdOrName}/uploadAttachment
            total_subidos = 0

            async with httpx.AsyncClient(timeout=120.0) as client:
                for columna, uploads in archivos_para_subir.items():
                    for up_file in uploads:
                        try:
                            # Verificar si es un UploadFile o ya fue leído
                            contenido = None
                            nombre_archivo = ""
                            tipo_contenido = "image/jpeg"

                            if hasattr(up_file, "seek"):
                                # Es un UploadFile, intentar leer
                                try:
                                    await up_file.seek(0)
                                    contenido = await up_file.read()
                                    nombre_archivo = up_file.filename
                                    tipo_contenido = (
                                        getattr(up_file, "content_type", "image/jpeg")
                                        or "image/jpeg"
                                    )
                                except Exception as e:
                                    print(
                                        f"   ⚠️ Error leyendo archivo {getattr(up_file, 'filename', 'unknown')}: {e}"
                                    )
                                    continue
                            else:
                                # Ya fue leído, no podemos hacer nada
                                print(
                                    f"   ⚠️ Archivo ya fue consumido: {str(up_file)[:50]}"
                                )
                                continue

                            if not contenido or not nombre_archivo:
                                print(f"   ⚠️ No se pudo obtener contenido del archivo")
                                continue

                            print(
                                f"🚀 Subiendo a Content API: {nombre_archivo} -> {columna} ({len(contenido)} bytes)"
                            )

                            # Usar ID de tabla para Content API
                            tabla_id = TABLE_NAME_TO_ID.get(
                                tabla_destino, tabla_destino
                            )
                            # URL encode de la columna
                            import urllib.parse

                            columna_encoded = urllib.parse.quote(columna)
                            url = f"https://content.airtable.com/v0/{BASE_ID}/{tabla_id}/{record_id}/{columna_encoded}/uploadAttachment"
                            print(f"   🔍 DEBUG URL: {url}")

                            # Content API requires Multipart
                            files = {
                                "file": (
                                    nombre_archivo,
                                    contenido,
                                    tipo_contenido,
                                )
                            }
                            headers = {"Authorization": f"Bearer {API_KEY}"}

                            resp = await client.post(url, headers=headers, files=files)

                            if resp.status_code in (200, 201):
                                total_subidos += 1
                                print(f"   ✅ Subido OK: {nombre_archivo}")
                            else:
                                archivos_fallidos.append(nombre_archivo)
                                print(
                                    f"   ❌ Error Content API ({resp.status_code}): {resp.text[:200]}"
                                )
                                archivos_fallidos.append(up_file.filename)
                                print(
                                    f"   ❌ Error Content API ({resp.status_code}): {resp.text}"
                                )

                        except Exception as upload_err:
                            archivos_fallidos.append(up_file.filename)
                            print(
                                f"   ❌ Excepción subiendo {up_file.filename}: {upload_err}"
                            )

            return {
                "status": "success",
                "id": id_gestion,
                "record_id": record_id,
                "message": f"Denuncia registrada exitosamente. Tu número de gestión es {id_gestion}.",
                "archivos_subidos": total_subidos,
                "archivos_fallidos": archivos_fallidos,
                "files_status": "ok"
                if not archivos_fallidos and total_subidos > 0
                else (
                    "none"
                    if total_subidos == 0 and not archivos_fallidos
                    else "partial"
                ),
            }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error creando registro en Airtable: {error_msg}")

            # Dar info útil para debugging
            if "Unknown field name" in error_msg:
                # Extraer nombre del campo problemático
                raise HTTPException(
                    status_code=500,
                    detail=f"Campo no encontrado en tabla '{tabla_destino}'. Verificar COLUMNA AIRTABLE en CONFIG_CAMPOS. Error: {error_msg}",
                )
            raise HTTPException(
                status_code=500, detail=f"Error guardando denuncia: {error_msg}"
            )

    except HTTPException:
        raise
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
