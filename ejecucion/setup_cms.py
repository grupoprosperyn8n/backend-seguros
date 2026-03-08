import requests
import json
import time

API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# 1. Configuración de Datos para Migrar
DEFAULT_CONFIG = {
    "accidente": {
        "Titulo": "Denuncia de Accidente",
        "Icono": "fa-car-crash",
        "Color": "var(--danger)",
        "campos": [
            { "id": "fecha", "label": "Fecha del Siniestro", "type": "date", "required": True, "orden": 1 },
            { "id": "hora", "label": "Hora Aprox. (00-23)", "type": "number", "min": 0, "max": 23, "required": True, "orden": 2 },
            { "id": "direccion", "label": "Lugar del Hecho (Dirección exacta)", "type": "text", "required": True, "orden": 3 },
            { "id": "localidad", "label": "Localidad", "type": "text", "required": True, "orden": 4 },
            { "id": "uso", "label": "Uso del Vehículo", "type": "select", "options": "PARTICULAR, COMERCIAL, REMIS-TAXI, UBER/CABIFY, REPARTO", "required": True, "orden": 5 },
            { "id": "relato", "label": "Relato detallado", "type": "textarea", "required": True, "placeholder": "Detalle...", "orden": 6 },
            { "id": "terceros", "label": "¿Hubo Terceros?", "type": "select", "options": "SI, NO", "required": True, "orden": 7 },
            { "id": "lesionados", "label": "¿Hubo Lesionados?", "type": "select", "options": "SI, NO", "required": True, "orden": 8 }
        ]
    },
    "robo-incendio": {
        "Titulo": "Denuncia de Robo o Incendio Total",
        "Icono": "fa-fire",
        "Color": "var(--warning)",
        "campos": [
            { "id": "fecha", "label": "Fecha del Hecho", "type": "date", "required": True, "orden": 1 },
            { "id": "hora", "label": "Hora Aprox.", "type": "time", "required": True, "orden": 2 },
            { "id": "direccion", "label": "Lugar del Hecho", "type": "text", "required": True, "orden": 3 },
            { "id": "tipo_hecho", "label": "Tipo de Hecho", "type": "select", "options": "ROBO TOTAL, INCENDIO TOTAL, HURTO", "required": True, "orden": 4 },
            { "id": "relato", "label": "Relato del Hecho", "type": "textarea", "required": True, "orden": 5 }
        ]
    },
    "robo-parcial": {
        "Titulo": "Robo Parcial (Ruedas / Cristales)",
        "Icono": "fa-tools",
        "Color": "var(--primary)",
        "campos": [
            { "id": "fecha", "label": "Fecha del Hecho", "type": "date", "required": True, "orden": 1 },
            { "id": "direccion", "label": "Lugar del Hecho", "type": "text", "required": True, "orden": 2 },
            { "id": "elemento", "label": "Elemento Sustraído", "type": "select", "options": "RUEDA DE AUXILIO, RUEDA PUESTA, CRISTAL LATERAL, PARABRISAS, LUNETA, CERRADURA, BATERIA", "required": True, "orden": 3 },
            { "id": "relato", "label": "Relato del Hecho", "type": "textarea", "required": True, "orden": 4 }
        ]
    }
}

def get_table_id(name):
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"❌ Error listando tablas: {resp.text}")
        return None
    
    for t in resp.json().get("tables", []):
        if t["name"] == name:
            return t["id"]
    return None

def create_campos_table(config_form_id):
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    payload = {
        "name": "CONFIG_CAMPOS",
        "description": "Campos de los formularios dinámicos",
        "fields": [
            { "name": "ID Campo", "type": "singleLineText", "description": "Identificador interno (ej: fecha, relato)" },
            { "name": "Etiqueta", "type": "singleLineText", "description": "Pregunta visible para el usuario" },
            { "name": "Tipo", "type": "singleSelect", "options": {
                "choices": [
                    {"name": "text"}, {"name": "textarea"}, {"name": "date"}, 
                    {"name": "time"}, {"name": "number"}, {"name": "select"}
                ]
            }},
            { "name": "Opciones", "type": "multilineText", "description": "Opciones separadas por coma (para Select)" },
            { "name": "Obligatorio", "type": "checkbox", "options": { "icon": "check", "color": "redBright" }},
            { "name": "Orden", "type": "number", "options": { "precision": 0 }},
            { "name": "Formulario", "type": "multipleRecordLinks", "options": { "linkedTableId": config_form_id }}
        ]
    }
    
    print("🚀 Creando tabla CONFIG_CAMPOS...")
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code == 200:
        print("✅ Tabla CONFIG_CAMPOS creada!")
        return True
    elif resp.status_code == 403:
        print("❌ Error de Permisos (403) - Tokens metadata.")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")
    return False

def populate_data():
    # 1. Get Config Records to Link
    print("📥 Obteniendo IDs de Formularios...")
    url_forms = f"https://api.airtable.com/v0/{BASE_ID}/CONFIG_FORMULARIOS"
    resp_forms = requests.get(url_forms, headers=HEADERS)
    form_map = {} # slug -> record_id
    
    if resp_forms.status_code == 200:
        for r in resp_forms.json().get("records", []):
            slug = r["fields"].get("Slug")
            if slug:
                form_map[slug] = r["id"]
    
    # 2. Populate Fields
    print("📤 Migrando Campos...")
    url_campos = f"https://api.airtable.com/v0/{BASE_ID}/CONFIG_CAMPOS"
    
    batch_records = []
    
    for slug, data in DEFAULT_CONFIG.items():
        form_id = form_map.get(slug)
        if not form_id:
            print(f"⚠️ Formulario {slug} no encontrado en Airtable (¿Ejecutaste el script anterior?)")
            continue
            
        for campo in data["campos"]:
            fields = {
                "ID Campo": campo["id"],
                "Etiqueta": campo["label"],
                "Tipo": campo["type"],
                "Orden": campo["orden"],
                "Formulario": [form_id],
                "Obligatorio": campo.get("required", False)
            }
            
            if "options" in campo:
                fields["Opciones"] = campo["options"]
                
            batch_records.append({"fields": fields})
            
            if len(batch_records) == 10:
                requests.post(url_campos, headers=HEADERS, json={"records": batch_records, "typecast": True})
                batch_records = []
                time.sleep(0.2) # Rate limit friendly

    if batch_records:
         requests.post(url_campos, headers=HEADERS, json={"records": batch_records, "typecast": True})
         
    print("✅ Migración completada.")

if __name__ == "__main__":
    cid = get_table_id("CONFIG_FORMULARIOS")
    if cid:
        campos_id = get_table_id("CONFIG_CAMPOS")
        if not campos_id:
            if create_campos_table(cid):
                populate_data()
        else:
            print("INFO: Tabla CONFIG_CAMPOS ya existe. Poblando datos...")
            populate_data()
    else:
        print("❌ CRITICAL: No existe CONFIG_FORMULARIOS. Creala primero.")
