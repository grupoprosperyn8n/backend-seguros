
import requests
import json
import os

TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

TABLES = [
    # Denuncias
    "DENUNCIA DE ACCIDENTE",
    "DENUNCIA ROBO OC", 
    "DENUNCIA ROBO / INCENDIO",
    
    # Core
    "CLIENTES",
    "EMPLEADOS",
    "OFICINAS", 
    "GESTIÓN GENERAL",
    "POLIZAS",
    "COMPANIA",
    "PRODUCTOS",
    "LOGIN"
]

def analyze_table_fields(table_name):
    print(f"\n--- Analizando: {table_name} ---")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    # URL Encode table_name manually if needed or requests does it
    # But names with / need manual encoding or requests will handle if we pass as path param
    # requests path params is tricky for / in path, so let's construct URL manually
    encoded_name = requests.utils.quote(table_name)
    url = f"https://api.airtable.com/v0/{BASE_ID}/{encoded_name}?maxRecords=50"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            
            if not records:
                print(f"✅ Tabla encontrada, pero vacía (0 registros). No se pueden inferir campos.")
                return None
            
            # Analyze fields from multiple records
            print(f"✅ Analizando {len(records)} registros para encontrar todos los campos posibles...")
            
            all_fields = {}
            for record in records:
                fields = record.get("fields", {})
                for k, val in fields.items():
                    if k not in all_fields:
                        # Determine type
                        val_type = type(val).__name__
                        if isinstance(val, list):
                            val_type = "List (Linked/Lookup/Multi)"
                        elif isinstance(val, bool):
                            val_type = "Checkbox"
                        elif isinstance(val, dict):
                            if "url" in val: val_type = "Attachment/Object"
                            else: val_type = "Object"
                        elif "T00:00:00.000Z" in str(val) or ("T" in str(val) and "Z" in str(val) and len(str(val)) > 10):
                             val_type = "Date/DateTime"
                        
                        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict) and "url" in val[0]:
                            val_type = "Attachment"
                            
                        all_fields[k] = val_type

            print(f"✅ Campos detectados totales ({len(all_fields)}):")
            sorted_fields = sorted(all_fields.keys())
            
            for k in sorted_fields:
                print(f"  - {k} [{all_fields[k]}]")
                
            return all_fields

        elif response.status_code == 404:
            # Try variations or declare missing
            print(f"❌ Tabla no encontrada (404). Nombre exacto incorrecto?")
            
            # Try lowercase or common variations
            # Only try basic variations if initial fails
            if table_name.isupper():
                print(f"🔄 Probando Capitalized: {table_name.title()}...")
                return analyze_table_fields(table_name.title())
            elif table_name[0].isupper():
                # Maybe lowercase?
                 pass
            
            return None
        else:
            print(f"⚠️ Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"🔥 Excepción: {e}")
        return None

def main():
    print("Iniciando Escaneo de Esquema Airtable...")
    
    full_schema = {}
    
    for table in TABLES:
        fields = analyze_table_fields(table)
        if fields:
            full_schema[table] = fields
            
    # Also verify specific problematic tables with known names from previous turns
    # "Denuncia de accidente" (Capitalized first letter only, lowercase rest?)
    # "Denuncia robo oc"
    # "Denuncia robo / incendio"
    
    print("\n--- Verificando nombres específicos de Webhooks anteriores ---")
    specific_tables = [
        "Denuncia de accidente",
        "Denuncia robo oc",
        "Denuncia robo / incendio"
    ]
    
    for table in specific_tables:
        # Check if already found
        found = False
        for k in full_schema.keys():
            if k.lower() == table.lower():
                found = True
        
        if not found:
            # Try exact name from JSON
            fields = analyze_table_fields(table)
            if fields:
                full_schema[table] = fields

    print("\n\n=== RESULTADO FINAL ===")
    print(json.dumps(full_schema, indent=2, ensure_ascii=False))
    
    # Save to json file for reference
    with open("schema_dump.json", "w") as f:
        json.dump(full_schema, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
