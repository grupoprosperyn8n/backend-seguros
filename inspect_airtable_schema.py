import requests

# Hardcoded credentials to avoid dotenv issues
API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

def get_table_schema(table_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}?maxRecords=1"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    print(f"\n--- INSPECCIONANDO TABLA: {table_name} ---")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return

    data = response.json()
    if "records" in data and len(data["records"]) > 0:
        fields = data["records"][0]["fields"].keys()
        print("Campos encontrados:")
        for f in fields:
            print(f" - {f}")
    else:
        print("Tabla vacía o no encontrada. No se pueden inferir campos.")

# Tablas probables basadas en el contexto
tablas_a_revisar = [
    "DENUNCIA DE ACCIDENTE",
    "DENUNCIA DE ROBO O INCENDIO TOTAL", 
    "DENUNCIA DE ROBO PARCIAL",
    "POLIZAS",
    "CLIENTES"
]

for t in tablas_a_revisar:
    get_table_schema(t)
