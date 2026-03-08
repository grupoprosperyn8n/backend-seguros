import requests
import json

API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

def get_data(table_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()

def debug():
    print("--- FORMULARIOS ---")
    data_f = get_data("CONFIG_FORMULARIOS")
    for r in data_f.get('records', []):
        f = r['fields']
        print(f"ID: {r['id']} | CODIGO: {f.get('CODIGO')} | VISIBILIDAD: {f.get('VISIBILIDAD')}")
    
    print("\n--- CAMPOS ---")
    data_c = get_data("CONFIG_CAMPOS")
    for r in data_c.get('records', []):
        f = r['fields']
        print(f"ID CAMPO: {f.get('ID CAMPO')} | FORMULARIO: {f.get('FORMULARIO')} | Formulario: {f.get('Formulario')}")

if __name__ == "__main__":
    debug()
