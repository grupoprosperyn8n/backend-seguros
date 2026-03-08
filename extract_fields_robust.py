import json
import sys

try:
    with open('/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/airtable_meta.json', 'r') as f:
        data = json.load(f)

    target_tables = [
        "DENUNCIA DE ACCIDENTE",
        "DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL",
        "CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )"
    ]

    for t in data['tables']:
        if t['name'] in target_tables:
            print(f"--- TABLE: {t['name']} ---")
            for f in t['fields']:
                print(f"  - {f['name']}")

except Exception as e:
    print(f"Error: {e}")
