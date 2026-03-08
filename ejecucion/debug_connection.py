import requests
import sys

API_TOKEN = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

print("Starting debug script...")
try:
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    print(f"Requesting {url}")
    resp = requests.get(url, headers={"Authorization": f"Bearer {API_TOKEN}"}, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Tables found:")
        for t in data.get("tables", []):
            print(f"- {t['name']} ({t['id']})")
            if t['name'] == 'CONFIG_CAMPOS':
                for f in t.get('fields', []):
                    if f['name'] == 'Tipo':
                        print(f"  -> Field 'Tipo' ID: {f['id']}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
print("End debug script.")
