
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not API_KEY or not BASE_ID:
    print("Error: Missing env vars")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def airtable_request(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

print(f"--- Inspeccionando Base {BASE_ID} ---")

# 1. Fetch CLIENTES record to see Linked Record Field
print("\n[CLIENTES] Buscando 1 registro...")
url_clientes = f"https://api.airtable.com/v0/{BASE_ID}/CLIENTES?maxRecords=1"
data = airtable_request(url_clientes)

linked_field_name = None
linked_rec_id = None

if data and 'records' in data and len(data['records']) > 0:
    r = data['records'][0]
    fields = r['fields']
    print(f"Registro encontrado: {r['id']}")
    
    # Buscar campo de link
    for k, v in fields.items():
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str) and v[0].startswith('rec'):
            print(f"  Field '{k}': {v} (Possible Link)")
            if "POLIZA" in k.upper() or "VEHICULO" in k.upper():
                linked_field_name = k
                linked_rec_id = v[0]
                print(f"  -> CANDIDATO DETECTADO: {k}")

else:
    print("No records or error in CLIENTES")

# 2. If we have a Record ID, try to find which table it belongs to
if linked_rec_id:
    print(f"\nIntentando identificar tabla para ID {linked_rec_id}...")
    candidates = ["POLIZAS", "Polizas", "Pólizas", "VEHICULOS", "Vehiculos", "AUTOS", "Autos", "VEHICULOS CLIENTES"]
    
    for table_name in candidates:
        encoded_table = urllib.parse.quote(table_name)
        url_rec = f"https://api.airtable.com/v0/{BASE_ID}/{encoded_table}/{linked_rec_id}"
        print(f"  Checking table '{table_name}'...")
        res = airtable_request(url_rec)
        if res and 'id' in res:
            print(f"  ✅ MATCH! La tabla es '{table_name}'")
            print(f"  Campos: {list(res['fields'].keys())}")
            break
