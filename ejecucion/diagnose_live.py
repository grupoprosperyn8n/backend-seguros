
import os
import requests
import re
from pyairtable import Table
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
API_URL = "https://web-production-2584d.up.railway.app/api/validate-siniestro"

def diagnose():
    print("--- 🕵️ DIAGNÓSTICO EN VIVO ---")
    
    # 1. Obtener un cliente REAL con datos de póliza
    print("\n1. Buscando datos reales en Airtable...")
    try:
        table = Table(API_KEY, BASE_ID, "CLIENTES")
        # Traer clientes con etiqueta no vacía
        formula = "NOT({ETIQUETA_POLIZA Compilación (de POLIZAS)}='')"
        records = table.all(formula=formula, max_records=5)
        
        target_dni = None
        target_patente = None
        target_etiqueta = None
        
        for r in records:
            f = r["fields"]
            etiqueta = f.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", "")
            dni = f.get("DNI")
            
            # Buscar patente en la etiqueta (Ej: 🏷️ AE123CD)
            # Regex flexible para capturar patente
            match = re.search(r'([A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})', etiqueta)
            
            if dni and match:
                target_dni = str(dni)
                target_patente = match.group(1)
                target_etiqueta = etiqueta
                print(f"✅ Caso Encontrado: DNI={target_dni}, Patente={target_patente}")
                print(f"📝 Etiqueta (truncada): {etiqueta[:50]}...")
                break
        
        if not target_dni:
            print("❌ No se encontró ningún cliente con etiqueta válida para probar.")
            return

        # 2. Probar Endpoint
        print(f"\n2. Probando Endpoint: {API_URL}")
        params = {"dni": target_dni, "patente": target_patente}
        print(f"📤 Enviando: {params}")
        
        try:
            resp = requests.get(API_URL, params=params, timeout=10)
            print(f"📥 Status Code: {resp.status_code}")
            
            try:
                data = resp.json()
                print(f"📦 Response Body:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if resp.status_code == 200:
                    if data.get("valid") and data.get("poliza", {}).get("numero"):
                        print("\n✅ EL FIX FUNCIONA: Se recuperaron datos de póliza.")
                    elif data.get("valid") is False:
                         print(f"\n⚠️ VALIDACIÓN FALLIDA: {data.get('message')}")
                         print("Posible causa: La etiqueta no coincide con el regex del backend o lógica de negocio.")
                    else:
                        print("\n⚠️ RESPUESTA INCOMPLETA: Valid true pero sin datos de póliza clave.")
                else:
                    print("\n❌ ERROR DE SERVIDOR: Revisa el 'detail' en el JSON arriba.")
                    
            except Exception as e:
                print(f"❌ Error parseando JSON response: {e}")
                print(f"Raw text: {resp.text}")

        except Exception as e:
            print(f"❌ Error conectando al backend: {e}")

    except Exception as e:
        print(f"❌ Error conectando a Airtable: {e}")

if __name__ == "__main__":
    diagnose()
