import httpx
import asyncio

# URL del webhook de n8n (tomada de tus logs)
N8N_WEBHOOK_SINIESTRO = "https://primary-production-0abcf.up.railway.app/webhook/crear-siniestro"

# Payload de prueba (simulando lo que envía el backend)
payload = {
    "tipo_formulario": "DENUNCIA_ART_ADMINISTRATIVO",
    "datos": {
        "descripcion": "Prueba de diagnóstico de respuesta n8n",
        "telefono": "123456789"
    },
    "archivos": {},
    "poliza_record_id": "recTEST123456",
    "dni": "12345678"
}

async def test_n8n():
    print(f"🚀 Enviando petición a: {N8N_WEBHOOK_SINIESTRO}")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                N8N_WEBHOOK_SINIESTRO,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
        print(f"📨 Status Code: {response.status_code}")
        print("🔍 Headers recibidos:")
        for k, v in response.headers.items():
            print(f"   {k}: {v}")
            
        print("\n📦 Cuerpo de la respuesta (RAW):")
        print("---------------------------------------------------")
        print(response.text)
        print("---------------------------------------------------")

        try:
            json_data = response.json()
            print("\n✅ El cuerpo es un JSON válido.")
            print(json_data)
        except Exception as e:
            print(f"\n❌ ERROR: El cuerpo NO es un JSON válido. Error: {e}")

    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    asyncio.run(test_n8n())
