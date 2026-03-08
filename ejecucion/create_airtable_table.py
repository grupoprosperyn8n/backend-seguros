import requests
import json

BASE_ID = "appuhslj3GFf60Tea"
API_TOKEN = "patXXX_REMOVED_XXX"

def create_table():
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": "CONFIG_FORMULARIOS",
        "description": "Configuración dinámica de formularios para la App de Seguros",
        "fields": [
            {
                "name": "Slug",
                "type": "singleLineText",
                "description": "Identificador único (ej: accidente, robo-parcial)"
            },
            {
                "name": "Titulo",
                "type": "singleLineText",
                "description": "Título visible del formulario"
            },
            {
                "name": "Icono",
                "type": "singleLineText",
                "description": "Clase de FontAwesome (ej: fa-car-crash)"
            },
            {
                "name": "Color",
                "type": "singleLineText",
                "description": "Color hexadecimal o variable CSS"
            },
            {
                "name": "Configuracion",
                "type": "multilineText",
                "description": "JSON con la definición de los campos"
            }
        ]
    }

    print(f"🚀 Intentando crear tabla en Base {BASE_ID}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ Tabla 'CONFIG_FORMULARIOS' creada exitosamente!")
            print(json.dumps(response.json(), indent=2))
        elif response.status_code == 403: # Forbidden
             error_data = response.json()
             print(f"❌ Error de Permisos (403): {error_data.get('error', {}).get('type')}")
             print("⚠️  Es probable que el token no tenga el scope 'schema.bases:write'.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

if __name__ == "__main__":
    create_table()
