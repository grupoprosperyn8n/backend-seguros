import requests
import json

API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"
TABLE_ID = "tblBJoFWFZxHo8zpq"
FIELD_ID = "fld3Irh5p4OMmdHpY"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# La lista completa solicitada
NEW_OPTIONS = [
    # Compatibilidad
    {"name": "text", "color": "blueLight2"},
    {"name": "textarea", "color": "blueLight2"},
    {"name": "date", "color": "cyanLight2"},
    {"name": "time", "color": "cyanLight2"},
    {"name": "number", "color": "tealLight2"},
    {"name": "select", "color": "yellowLight2"},
    
    # Nuevos
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
    {"name": "linkedRecord", "color": "pink"},
    {"name": "lookup", "color": "pink"},
    {"name": "rollup", "color": "pink"},
    {"name": "formula", "color": "gray"},
    {"name": "user", "color": "gray"},
    {"name": "createdBy", "color": "gray"},
    {"name": "lastModifiedBy", "color": "gray"},
    {"name": "autoNumber", "color": "gray"},
    {"name": "createdTime", "color": "gray"},
    {"name": "lastModifiedTime", "color": "gray"}
]

def update_direct():
    print(f"🚀 Actualizando campo {FIELD_ID} directamente...")
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields/{FIELD_ID}"
    
    payload = {
        "options": {
            "choices": NEW_OPTIONS
        }
    }
    
    try:
        print("Enviando request...")
        resp = requests.patch(url, headers=HEADERS, json=payload, timeout=30)
        print(f"Response received. Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print("✅ ¡Opciones actualizadas exitosamente!")
        else:
            print(f"❌ Error actualizando campo: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Error de conexión/timeout: {e}")

if __name__ == "__main__":
    update_direct()
