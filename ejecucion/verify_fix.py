
import os
import requests
import re
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
# URL Backend Production
API_URL = "https://web-production-2584d.up.railway.app/api/validate-siniestro"

def get_test_case():
    print("🔍 Buscando cliente con pólizas en Airtable...")
    table = Table(API_KEY, BASE_ID, "CLIENTES")
    # Traer clientes que tengan algo en la etiqueta de poliza
    formula = "NOT({ETIQUETA_POLIZA Compilación (de POLIZAS)}='')"
    records = table.all(formula=formula, max_records=10)
    
    for r in records:
        f = r["fields"]
        dni = f.get("DNI")
        etiqueta = f.get("ETIQUETA_POLIZA Compilación (de POLIZAS)")
        
        if dni and etiqueta:
            # Intentar extraer una patente de la etiqueta
            # Buscamos patrón simple de 6 bu 7 caracteres alfanuméricos
            # Ojo: la etiqueta tiene emojis, etc.
            # E.g. "✅ vige... 🏷️ AE123CD ..."
            match = re.search(r'([A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})', str(etiqueta))
            if match:
                patente = match.group(1)
                print(f"✅ Caso encontrado: DNI={dni}, Patente={patente}")
                return dni, patente
                
    print("❌ No se encontraron casos de prueba aptos.")
    return None, None

def test_endpoint(dni, patente):
    print(f"🚀 Probando API: {API_URL}")
    print(f"👉 DNI: {dni}, Patente: {patente}")
    
    try:
        resp = requests.get(API_URL, params={"dni": dni, "patente": patente})
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print("📦 Respuesta JSON:")
            import json
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get("valid") == True and data.get("poliza", {}).get("numero"):
                print("\n✅ ÉXITO: La API retornó la póliza correctamente parseada.")
                print(f"   - Poliza N°: {data['poliza']['numero']}")
                print(f"   - Vehiculo: {data['poliza']['tipo_vehiculo']}")
            else:
                print("\n⚠️ ALERTA: La validación pasó pero faltan datos o valid=False.")
        else:
            print(f"❌ Error API: {resp.text}")
            
    except Exception as e:
        print(f"❌ Excepción request: {e}")

if __name__ == "__main__":
    dni, patente = get_test_case()
    if dni and patente:
        test_endpoint(dni, patente)
