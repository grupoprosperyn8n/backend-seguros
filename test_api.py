import requests

url = "https://web-production-2584d.up.railway.app/api/faqs"
try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(response.json())
except Exception as e:
    print(e)
