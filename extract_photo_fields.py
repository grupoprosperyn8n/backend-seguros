import json

def extract_photo_fields():
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
                    # Buscamos campos de archivo o que parezcan fotos
                    if f.get('type') == 'multipleAttachments' or 'FOTO' in f['name'].upper():
                        print(f"  - {f['name']} ({f['type']})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_photo_fields()
