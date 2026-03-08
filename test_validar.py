import requests

url = "https://web-production-2584d.up.railway.app/api/validar-cliente"
payload = {
    "dni": "43770731",
    "patente": "234RTY"
}

try:
    response = requests.post(url, json=payload)
    print(response.status_code)
    print(response.json())
except Exception as e:
    print("Error:", e)
