
import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_full_submission():
    url = "https://web-production-2584d.up.railway.app/api/create-siniestro"
    
    # Datos de prueba (Usa un DNI real para vinculación)
    dni_prueba = "26322995" 
    patente_prueba = "PDL384"
    
    # Simulamos el FormData
    data = {
        "tipo_formulario": "siniestro_auto",
        "dni": dni_prueba,
        "poliza_record_id": "recN9l3G9K6V3P9pB", # ID real de póliza si es posible
        "datos": json.dumps({
            "f_fecha": "2026-03-04",
            "f_hora": "15:30",
            "f_lugar": "Av. Corrientes 1234",
            "f_localidad": "CABA",
            "f_uso_vehiculo": "Particular",
            "f_relato": "Prueba técnica de carga v2.3 con archivos adjuntos.",
            "f_terceros": "No",
            "f_lesionados": "No"
        })
    }
    
    # Leer archivo local
    image_path = "/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/test_image.jpg"
    
    print(f"🚀 Enviando prueba integral a {url}...")
    
    files = []
    # Mapeamos a las columnas de Airtable según el field_map detectado
    # f_foto_dni -> FOTO DNI
    # f_foto_cedula -> FOTO CEDULA
    # f_foto_carnet -> FOTO CARNET
    
    try:
        with open(image_path, "rb") as f:
            img_content = f.read()
            # Simulamos múltiples campos de archivo
            files = [
                ("f_foto_dni", ("dni.jpg", img_content, "image/jpeg")),
                ("f_foto_cedula", ("cedula.jpg", img_content, "image/jpeg")),
                ("f_foto_carnet", ("carnet.jpg", img_content, "image/jpeg"))
            ]
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, data=data, files=files)
                print(f"STATUS: {response.status_code}")
                print(f"RESPONSE: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
                
                if response.status_code == 200:
                    print("✅ ÉXITO TOTAL: El backend procesó datos e imágenes.")
                else:
                    print("❌ ERROR EN PROCESAMIENTO.")
                    
    except Exception as e:
        print(f"🚨 EXCEPCIÓN: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_full_submission())
