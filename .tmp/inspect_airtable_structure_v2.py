
import os
from pyairtable import Table, Api
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not API_KEY or not BASE_ID:
    print("Error: Missing env vars")
    exit(1)

api = Api(API_KEY)

print(f"--- Buscando tablas en Base {BASE_ID} ---")
try:
    # Listar tablas si es posible con metadatos API (requiere token type correcto)
    # Si falla, probamos nombres comunes
    tables = ["POLIZAS", "Polizas", "Pólizas", "VEHICULOS", "Vehiculos", "AUTOS", "Autos"]
    
    found = False
    
    # 1. Inspeccionar CLIENTES para ver el campo link
    print("\n[CLIENTES] Inspeccionando registro de ejemplo...")
    t_clientes = api.table(BASE_ID, "CLIENTES")
    records = t_clientes.all(max_records=1)
    if records:
        r = records[0]
        # Buscar campos que parezcan links a pólizas
        for k, v in r['fields'].items():
            if "POLIZA" in k.upper() or "VEHICULO" in k.upper():
                print(f"  Field '{k}': {str(v)[:100]} (Tipo: {type(v)})")
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str) and v[0].startswith('rec'):
                    print(f"  -> POSIBLE LINK DETECTADO. ID ejemplo: {v[0]}")
                    # Intentar resolver ese ID en las tablas candidatas
                    for candidate in tables:
                        try:
                           t_cand = api.table(BASE_ID, candidate)
                           linked_rec = t_cand.get(v[0])
                           if linked_rec:
                               print(f"  ✅ MATCH! El ID {v[0]} pertenece a la tabla '{candidate}'")
                               print(f"  Campos de '{candidate}': {list(linked_rec['fields'].keys())}")
                               found = True
                               break
                        except:
                            pass
                    if found: break

    if not found:
        print("\nNo se pudo determinar automáticamente la tabla de pólizas.")
        
except Exception as e:
    print(f"Error: {e}")
