import os
import json
import requests
import time

# Configuration
API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"
TABLE_FORMS = "CONFIG_FORMULARIOS"
TABLE_FIELDS = "CONFIG_CAMPOS"

# DEFINICIÓN DE FORMULARIOS Y SUS CAMPOS
# Incluye 'airtable_column' para el mapeo dinámico en Backend
forms_data = {
    "accidente": {
        "titulo": "Denuncia de Accidente",
        "icono": "fa-car-crash",
        "color": "#e74c3c",
        "target_table": "DENUNCIA DE ACCIDENTE",
        "campos": [
            {"id": "fecha", "label": "Fecha del Siniestro", "type": "date", "required": True, "airtable_column": "FECHA DEL SINIESTRO"},
            {"id": "hora", "label": "Hora Aprox. (00-23)", "type": "number", "required": True, "airtable_column": "HORA APROX. DEL SINIESTRO"},
            {"id": "direccion", "label": "Lugar del Hecho", "type": "text", "required": True, "airtable_column": "LUGAR O ESTABLECIMIENTO"},
            {"id": "localidad", "label": "Localidad", "type": "text", "required": True, "airtable_column": "CIUDAD"}, 
            {"id": "uso", "label": "Uso del Vehículo", "type": "select", "options": "PARTICULAR,COMERCIAL,REMIS-TAXI", "required": True, "airtable_column": "USO DEL VEHICULO"},
            {"id": "relato", "label": "Relato del Hecho", "type": "textarea", "required": True, "airtable_column": "RELATOS DEL HECHO"},
            {"id": "terceros", "label": "¿Hubo Terceros?", "type": "select", "options": "SI,NO", "required": True, "airtable_column": "HUBO TERCEROS"},
            {"id": "lesionados", "label": "¿Hubo Lesionados?", "type": "select", "options": "SI,NO", "required": True, "airtable_column": "HUBO LESIONADOS"},
            
            # ADJUNTOS (FOTOS)
            {"id": "foto_dni", "label": "Foto DNI (Ambos Lados)", "type": "file", "required": True, "airtable_column": "FOTO DNI AMBOS LADOS"},
            {"id": "foto_cedula", "label": "Foto Cédula (Ambos Lados)", "type": "file", "required": True, "airtable_column": "FOTO CEDULA VERDE AMBOS LADOS"},
            {"id": "foto_carnet", "label": "Foto Carnet (Ambos Lados)", "type": "file", "required": True, "airtable_column": "FOTO CARNET CONDUCIR AMBOS LADOS"},
            {"id": "fotos_dano", "label": "Fotos Daños (Máx 3)", "type": "file", "required": True, "airtable_column": "FOTO DAÑO DEL VEHICULO X 3"}
        ]
    },
    "robo-incendio": {
        "titulo": "Robo / Incendio",
        "icono": "fa-fire",
        "color": "#e67e22",
        "target_table": "DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL",
        "campos": [
            {"id": "fecha", "label": "Fecha del Siniestro", "type": "date", "required": True, "airtable_column": "FECHA DEL SINIESTRO"},
            {"id": "hora", "label": "Hora Aprox.", "type": "time", "required": True, "airtable_column": "HORA APROX. DEL SINIESTRO"},
            {"id": "direccion", "label": "Lugar del Hecho", "type": "text", "required": True, "airtable_column": "LUGAR O ESTABLECIMIENTO"},
            {"id": "tipo_hecho", "label": "Tipo", "type": "select", "options": "ROBO TOTAL,INCENDIO TOTAL,INCENDIO PARCIAL", "required": True, "airtable_column": "CLASIFICACIÓN"},
            {"id": "relato", "label": "Relato", "type": "textarea", "required": True, "airtable_column": "RELATO DEL HECHO"},
            
             # ADJUNTOS
            {"id": "foto_dni", "label": "Foto DNI", "type": "file", "required": True, "airtable_column": "FOTO DNI AMBOS LADOS"},
            {"id": "foto_cedula", "label": "Foto Cédula", "type": "file", "required": True, "airtable_column": "FOTO CEDULA VERDE AMBOS LADOS"},
             {"id": "foto_carnet", "label": "Foto Carnet", "type": "file", "required": True, "airtable_column": "FOTO CARNET CONDUCIR AMBOS LADOS"}
        ]
    },
    "robo-parcial": {
        "titulo": "Robo Parcial (Ruedas/Cristales)",
        "icono": "fa-mask",
        "color": "#8e44ad",
        "target_table": "CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )",
        "campos": [
            {"id": "fecha", "label": "Fecha", "type": "date", "required": True, "airtable_column": "FECHA DEL SINIESTRO"},
            {"id": "direccion", "label": "Lugar del Hecho", "type": "text", "required": True, "airtable_column": "LUGAR O ESTABLECIMIENTO"},
            {"id": "elemento", "label": "Elemento Sustraído", "type": "select", "options": "RUEDA,CRISTAL,CERRADURA,BATERIA", "required": True, "airtable_column": "ELEMENTO"},
             {"id": "relato", "label": "Relato", "type": "textarea", "required": True, "airtable_column": "RELATO DEL HECHO"},
             
             # ADJUNTOS
            {"id": "foto_dni", "label": "Foto DNI", "type": "file", "required": True, "airtable_column": "FOTO DNI AMBOS LADOS"},
             {"id": "fotos_dano", "label": "Fotos Daños", "type": "file", "required": True, "airtable_column": "FOTO DAÑO DEL VEHICULO X 3"}
        ]
    }
}

def get_headers():
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

def clear_table(table_name):
    print(f"🧹 Limpiando tabla {table_name}...")
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    
    # Get all records
    records = []
    offset = None
    while True:
        params = {}
        if offset: params["offset"] = offset
        r = requests.get(url, headers=get_headers(), params=params)
        if r.status_code != 200: break
        data = r.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset: break
        
    # Delete in batches of 10
    ids_to_delete = [r["id"] for r in records]
    for i in range(0, len(ids_to_delete), 10):
        batch = ids_to_delete[i:i+10]
        params = [("records[]", rid) for rid in batch]
        requests.delete(url, headers=get_headers(), params=params)
        time.sleep(0.5)
    print(f"✅ Tabla {table_name} limpiada.")

def populate_relational():
    # 1. Limpiar ambas tablas para asegurar consistencia
    clear_table(TABLE_FIELDS) # Primero campos por FK
    clear_table(TABLE_FORMS)
    
    print("🚀 Iniciando carga relacional...")
    
    url_forms = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_FORMS}"
    url_fields = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_FIELDS}"
    
    for slug, data in forms_data.items():
        print(f"📝 Creando Formulario: {slug}")
        
        # 2. Crear Registro de Formulario
        form_payload = {
            "fields": {
                "CODIGO": slug,
                "ICONO": data["icono"],
                "TITULO": data["titulo"],
                "COLOR": data["color"],
                "TABLA RELACIONADA": data.get("target_table", ""),
                "VISIBILIDAD": True
                # "Configuracion": Removed as per user request
            }
        }
        
        r_form = requests.post(url_forms, headers=get_headers(), json=form_payload)
        if r_form.status_code != 200:
            print(f"❌ Error creando formulario {slug}: {r_form.text}")
            continue
            
        form_id = r_form.json()["id"]
        
        # 3. Crear Campos vinculados
        print(f"   ↳ Agregando {len(data['campos'])} campos...")
        
        fields_batch = []
        for i, campo in enumerate(data["campos"]):
            fields_batch.append({
                "fields": {
                    "ID CAMPO": campo["id"],
                    "ETIQUETA": campo["label"],
                    "TIPO": campo["type"],
                    "ORDEN": i,
                    "OBLIGATORIO": campo.get("required", False),
                    "OPCIONES": campo.get("options", ""),
                    "AIRTABLE COLUMN": campo.get("airtable_column", ""),
                    "Formulario": [form_id] # ✨ RELACIÓN MÁGICA
                }
            })
            
            # Batch de 10
            if len(fields_batch) == 10:
                requests.post(url_fields, headers=get_headers(), json={"records": fields_batch, "typecast": True})
                fields_batch = []
                time.sleep(0.2)
        
        # Remanente
        if fields_batch:
            requests.post(url_fields, headers=get_headers(), json={"records": fields_batch, "typecast": True})
            
    print("✨ Carga Relacional Completa!")

if __name__ == "__main__":
    populate_relational()
