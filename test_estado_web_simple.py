#!/usr/bin/env python3
"""
Script simple para verificar ESTADO_WEB con requests
"""

import requests
import json

# Credenciales
API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("=" * 80)
print("🧪 VERIFICACIÓN: Campo ESTADO_WEB")
print("=" * 80)

# 1. Obtener schema del campo
print("\n1️⃣ Obteniendo opciones válidas del campo ESTADO_WEB...")

meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.get(meta_url, headers=HEADERS)

if response.status_code == 200:
    tables = response.json().get("tables", [])

    for table_info in tables:
        if table_info["name"] in ["DENUNCIA DE ACCIDENTE", "DENUNCIA ROBO OC", "DENUNCIA ROBO / INCENDIO"]:
            print(f"\n📋 Tabla: {table_info['name']}")

            for field in table_info.get("fields", []):
                if field["name"] == "ESTADO_WEB":
                    print(f"   ✅ Campo ESTADO_WEB encontrado")
                    print(f"   Tipo: {field.get('type')}")

                    if field.get("type") == "singleSelect":
                        choices = field.get("options", {}).get("choices", [])
                        print(f"   Opciones válidas ({len(choices)}):")
                        for idx, choice in enumerate(choices, 1):
                            choice_name = choice.get("name")
                            print(f"      {idx}. '{choice_name}'")
                    break
else:
    print(f"❌ Error: {response.status_code} - {response.text}")

# 2. Leer algunos registros para ver valores reales
print("\n\n2️⃣ Leyendo registros existentes...")

tabla_url = f"https://api.airtable.com/v0/{BASE_ID}/DENUNCIA DE ACCIDENTE"
params = {"maxRecords": 3, "fields[]": ["ESTADO_WEB", "ID_GESTION_UNICO"]}

response = requests.get(tabla_url, headers=HEADERS, params=params)

if response.status_code == 200:
    records = response.json().get("records", [])
    print(f"✅ Encontrados {len(records)} registros\n")

    for rec in records:
        fields = rec.get("fields", {})
        estado = fields.get("ESTADO_WEB", "❌ No definido")
        id_gest = fields.get("ID_GESTION_UNICO", "N/A")

        print(f"   📄 {id_gest}")
        print(f"      ESTADO_WEB: '{estado}'")

        if estado != "❌ No definido":
            # Analizar el valor
            tiene_emoji = any(emoji in str(estado) for emoji in ["🆕", "👀", "✅"])
            print(f"      Tiene emoji: {tiene_emoji}")
        print()
else:
    print(f"❌ Error: {response.status_code}")

# 3. Análisis
print("\n" + "=" * 80)
print("📊 ANÁLISIS DE COMPATIBILIDAD")
print("=" * 80)

backend_value = "NUEVO WEB"
print(f"\n🔧 Backend envía: '{backend_value}'")
print(f"🎯 Airtable espera una de: '🆕 NUEVO WEB', '👀 VISTO', '✅ PROCESADO'")

print(f"\n❓ ¿Coinciden?")
print(f"   '{backend_value}' == '🆕 NUEVO WEB': {backend_value == '🆕 NUEVO WEB'}")
print(f"   '{backend_value}' in '🆕 NUEVO WEB': {backend_value in '🆕 NUEVO WEB'}")

print("\n" + "=" * 80)
print("💡 RECOMENDACIONES")
print("=" * 80)

print("""
1️⃣ PROBLEMA IDENTIFICADO:
   El backend envía "NUEVO WEB" pero Airtable espera "🆕 NUEVO WEB" (con emoji)

2️⃣ SOLUCIÓN:
   Cambiar línea 981 en backend/main.py:

   DE:
     airtable_payload["ESTADO_WEB"] = "NUEVO WEB"

   A:
     airtable_payload["ESTADO_WEB"] = "🆕 NUEVO WEB"

3️⃣ COMPORTAMIENTO ACTUAL:
   Con typecast=True, Airtable puede:
   - Crear una opción nueva "NUEVO WEB" (sin emoji) ⚠️
   - Hacer match aproximado si ignora emojis ✅
   - Dejar el campo vacío si no hay match ❌

   Para evitar ambigüedad, usar el valor exacto con emoji.
""")
