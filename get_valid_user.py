import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

t_clientes = Table(API_KEY, BASE_ID, "CLIENTES")
t_polizas = Table(API_KEY, BASE_ID, "POLIZAS")

# Buscamos un cliente que tenga polizas
clientes = t_clientes.all(max_records=50)
for c in clientes:
    if "DNI" in c["fields"] and "POLIZAS" in c["fields"]:
        dni = c["fields"]["DNI"]
        polizas_ids = c["fields"]["POLIZAS"]
        
        for pid in polizas_ids:
            try:
                pol = t_polizas.get(pid)
                if "PATENTE" in pol["fields"] or "Patente" in pol["fields"] or "PATENTE (auto)" in pol["fields"]:
                    # Imprimir todos los campos para ver como se llama la patente
                    print(f"ENCONTRADO: DNI={dni}, POLIZA={pol['fields']}")
                    exit(0)
            except Exception as e:
                pass
print("No se encontro un par DNI/Patente valido facilmente.")
