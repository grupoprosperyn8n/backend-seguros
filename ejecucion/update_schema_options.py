import requests
import json

API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"
TABLE_NAME = "CONFIG_CAMPOS"
FIELD_NAME = "Tipo"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# La lista completa solicitada por el usuario + los existentes para compatibilidad
NEW_OPTIONS = [
    # Existentes (MANTENER para no romper app)
    {"name": "text", "color": "blueLight2"},
    {"name": "textarea", "color": "blueLight2"},
    {"name": "date", "color": "cyanLight2"},
    {"name": "time", "color": "cyanLight2"},
    {"name": "number", "color": "tealLight2"},
    {"name": "select", "color": "yellowLight2"},
    
    # Nuevos (Mapeados del pedido del usuario)
    {"name": "singleLineText", "color": "blue"},
    {"name": "longText", "color": "blue"},
    {"name": "richText", "color": "blueDark"},
    
    {"name": "currency", "color": "green"},
    {"name": "percent", "color": "green"},
    {"name": "rating", "color": "orange"},
    {"name": "duration", "color": "orange"},
    
    {"name": "dateTime", "color": "cyan"},
    
    {"name": "multiselect", "color": "yellow"},
    
    {"name": "email", "color": "red"},
    {"name": "phone", "color": "red"},
    {"name": "url", "color": "red"},
    
    {"name": "attachment", "color": "purple"},
    
    {"name": "checkbox", "color": "gray"},
    {"name": "barcode", "color": "gray"},
    {"name": "button", "color": "gray"},
    {"name": "aiText", "color": "purpleDark"},
    
    # Relacionales / Avanzados
    {"name": "linkedRecord", "color": "pink"},
    {"name": "lookup", "color": "pink"},
    {"name": "rollup", "color": "pink"},
    {"name": "formula", "color": "gray"},
    
    # Metadata
    {"name": "user", "color": "gray"},
    {"name": "createdBy", "color": "gray"},
    {"name": "lastModifiedBy", "color": "gray"},
    {"name": "autoNumber", "color": "gray"},
    {"name": "createdTime", "color": "gray"},
    {"name": "lastModifiedTime", "color": "gray"}
]

def get_table_id(base_id, table_name):
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        for t in resp.json().get("tables", []):
            if t["name"] == table_name:
                return t["id"]
    return None

def get_field_id(base_id, table_id, field_name):
    # La API de listar tablas ya devuelve campos en algunas versiones, pero mejor asegurar URL
    # En meta API, GET tables devuelve los campos tambien.
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        for t in resp.json().get("tables", []):
            if t["id"] == table_id:
                for f in t.get("fields", []):
                    if f["name"] == field_name:
                        return f["id"]
    return None

def update_field_options():
    print(f"🔍 Buscando tabla '{TABLE_NAME}'...")
    table_id = get_table_id(BASE_ID, TABLE_NAME)
    if not table_id:
        print(f"❌ No encontré la tabla {TABLE_NAME}")
        return

    print(f"🔍 Buscando campo '{FIELD_NAME}'...")
    field_id = get_field_id(BASE_ID, table_id, FIELD_NAME)
    if not field_id:
        print(f"❌ No encontré el campo {FIELD_NAME}")
        return

    print(f"🚀 Actualizando opciones para {FIELD_NAME} ({field_id})...")
    
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{table_id}/fields/{field_id}"
    
    payload = {
        "options": {
            "choices": NEW_OPTIONS
        }
    }
    
    resp = requests.patch(url, headers=HEADERS, json=payload)
    
    if resp.status_code == 200:
        print("✅ ¡Opciones actualizadas exitosamente!")
        print(f"Ahora tenés {len(NEW_OPTIONS)} tipos de campo disponibles.")
    else:
        print(f"❌ Error actualizando campo: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    update_field_options()
