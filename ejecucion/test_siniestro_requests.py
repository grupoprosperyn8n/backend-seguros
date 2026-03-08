
import requests
import json
import os

def test_full_submission():
    url = "https://web-production-2584d.up.railway.app/api/create-siniestro"
    
    dni_prueba = "26322995" 
    patente_prueba = "PDL384"
    
    data = {
        "tipo_formulario": "accidente",
        "dni": dni_prueba,
        "poliza_record_id": "recM1AvePIvUt6ZO2",
        "datos": json.dumps({
            "f_fecha": "2026-03-04",
            "f_hora": "15:30",
            "f_lugar": "Av. Corrientes 1234",
            "f_localidad": "CABA",
            "f_uso_vehiculo": "Particular",
            "f_relato": "Prueba técnica de carga v2.3 con ARCHIVOS ADJUNTOS vía Requests.",
            "f_terceros": "No",
            "f_lesionados": "No"
        })
    }
    
    image_path = "/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/test_image.jpg"
    
    print(f"🚀 Enviando prueba integral a {url}...")
    
    try:
        with open(image_path, "rb") as f:
            img_content = f.read()
            files = [
                ("f_foto_dni", ("dni.jpg", img_content, "image/jpeg")),
                ("f_foto_cedula", ("cedula.jpg", img_content, "image/jpeg")),
                ("f_foto_carnet", ("carnet.jpg", img_content, "image/jpeg"))
            ]
            
            response = requests.post(url, data=data, files=files, timeout=60)
            print(f"STATUS: {response.status_code}")
            print(f"RESPONSE: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ ÉXITO TOTAL: El backend procesó datos e imágenes.")
            else:
                print("❌ ERROR EN PROCESAMIENTO.")
                
    except Exception as e:
        print(f"🚨 EXCEPCIÓN: {str(e)}")

if __name__ == "__main__":
    test_full_submission()
