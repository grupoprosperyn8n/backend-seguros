
import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not API_KEY or not BASE_ID:
    print("Error: Missing env vars")
    exit(1)

def inspect_table(table_name):
    print(f"\n--- Inspecting {table_name} ---")
    try:
        table = Table(API_KEY, BASE_ID, table_name)
        records = table.all(max_records=1)
        if records:
            r = records[0]
            print(f"Campos encontrados en {table_name}:")
            for k, v in r["fields"].items():
                print(f" - {k}: {str(v)[:50]}...")
            return r
        else:
            print("No records found.")
            return None
    except Exception as e:
        print(f"Error accessing {table_name}: {e}")
        return None

# Inspect CLIENTES to see link fields
client_record = inspect_table("CLIENTES")

# Try to guess POLIZAS table name
polizas_names = ["POLIZAS", "Polizas", "Pólizas", "Vehic", "VEHICULOS", "AUTOS"]
for name in polizas_names:
    print(f"\nChecking table '{name}'...")
    try:
        t = Table(API_KEY, BASE_ID, name)
        # Try to fetch one record to confirm existence
        recs = t.all(max_records=1)
        if recs:
            print(f"FOUND Table '{name}'!")
            r = recs[0]
            print(f"Campos: {list(r['fields'].keys())}")
            break
    except:
        pass
