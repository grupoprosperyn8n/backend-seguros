import requests
import json

# URL del backend
BASE_URL = "https://web-production-2584d.up.railway.app"
ENDPOINT = f"{BASE_URL}/api/create-siniestro"

# Datos de prueba
payload = {
    "tipo_formulario": "accidente",
    "poliza_record_id": "recTestPoliza123", # Dummy ID
    "dni": "12345678",
    "patente": "ABC123",
    "datos": json.dumps({
        "fecha": "2023-10-27",
        "hora": "12:00",
        "direccion": "Calle Falsa 123",
        "localidad": "Rosario",
        "uso": "PARTICULAR",
        "relato": "Prueba de subida de archivos desde script",
        "terceros": "NO",
        "lesionados": "NO"
    })
}

# Archivo dummy pequeño
files = {
    'foto_dni': ('test_image.txt', 'Contenido de prueba de imagen', 'text/plain')
}

print(f"📡 Enviando solicitud a {ENDPOINT}...")

try:
    response = requests.post(ENDPOINT, data=payload, files=files, timeout=60)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Subida exitosa!")
    else:
        print("❌ Falló la subida.")

except Exception as e:
    print(f"❌ Error de conexión: {e}")
