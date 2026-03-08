import os
from pyairtable import Table, Api
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

tablas = [
    "DENUNCIA DE ACCIDENTE",
    "DENUNCIA ROBO / INCENDIO", 
    "DENUNCIA ROBO OC"
]

print(f"🕵️  Analizando tablas en Base: {BASE_ID}")

for nombre_tabla in tablas:
    print(f"\n--- {nombre_tabla} ---")
    try:
        table = Table(API_KEY, BASE_ID, nombre_tabla)
        # Traer 1 registro para ver las columnas
        records = table.all(max_records=1)
        if records:
            fields = records[0]["fields"].keys()
            print("✅ Columnas detectadas:")
            for f in sorted(fields):
                print(f"  - {f}")
        else:
            print("⚠️  Tabla vacía, no se pueden inferir columnas (se necesita al menos 1 registro)")
            
    except Exception as e:
        print(f"❌ Error accediendo: {e}")
