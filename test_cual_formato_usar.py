#!/usr/bin/env python3
"""
Script para determinar cuál formato de ESTADO_WEB usar
Compara ambos formatos con las opciones reales en Airtable
"""

import requests
import sys

API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

print("=" * 80)
print("🔍 DETERMINAR FORMATO CORRECTO DE ESTADO_WEB")
print("=" * 80)

# 1. Leer opciones del Meta API
print("\n1️⃣ Leyendo opciones desde Airtable Meta API...")

meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(meta_url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    sys.exit(1)

tables = response.json().get("tables", [])
opciones_reales = []

for table in tables:
    if table["name"] == "DENUNCIA DE ACCIDENTE":
        for field in table.get("fields", []):
            if field["name"] == "ESTADO_WEB":
                choices = field.get("options", {}).get("choices", [])
                opciones_reales = [choice.get("name") for choice in choices]
                break
        break

if not opciones_reales:
    print("❌ No se encontró el campo ESTADO_WEB")
    sys.exit(1)

print(f"✅ Opciones encontradas: {len(opciones_reales)}")

# 2. Definir los formatos a probar
print("\n2️⃣ Comparando formatos...")

formatos = {
    "CON_ESPACIO": {
        "NUEVO_WEB": "🆕 NUEVO WEB",
        "VISTO": "👀 VISTO",
        "PROCESADO": "✅ PROCESADO"
    },
    "SIN_ESPACIO": {
        "NUEVO_WEB": "🆕NUEVO WEB",
        "VISTO": "👀VISTO",
        "PROCESADO": "✅PROCESADO"
    }
}

# 3. Verificar matches
resultados = {}

for nombre_formato, valores in formatos.items():
    matches = 0
    detalles = []

    for key, valor in valores.items():
        match = valor in opciones_reales
        matches += match
        detalles.append({
            "key": key,
            "valor": valor,
            "match": match
        })

    resultados[nombre_formato] = {
        "matches": matches,
        "detalles": detalles,
        "completo": matches == len(valores)
    }

# 4. Mostrar resultados
print("\n" + "=" * 80)
print("📊 RESULTADOS")
print("=" * 80)

for nombre_formato, resultado in resultados.items():
    print(f"\n{'CON' if 'CON' in nombre_formato else 'SIN'} ESPACIO:")
    print(f"   Matches: {resultado['matches']}/{len(formatos[nombre_formato])}")

    for detalle in resultado["detalles"]:
        simbolo = "✅" if detalle["match"] else "❌"
        print(f"   {simbolo} {detalle['key']}: \"{detalle['valor']}\"")

    if resultado["completo"]:
        print(f"   🎯 FORMATO CORRECTO")

# 5. Determinar cuál usar
print("\n" + "=" * 80)
print("💡 RECOMENDACIÓN")
print("=" * 80)

if resultados["CON_ESPACIO"]["completo"]:
    print("""
✅ USAR FORMATO CON ESPACIO

En backend/main.py:
    USAR_CON_ESPACIO = True  # ← Dejar así

Valores que se usarán:
    "🆕 NUEVO WEB"
    "👀 VISTO"
    "✅ PROCESADO"
""")
elif resultados["SIN_ESPACIO"]["completo"]:
    print("""
✅ USAR FORMATO SIN ESPACIO

En backend/main.py:
    USAR_CON_ESPACIO = False  # ← CAMBIAR A FALSE

Valores que se usarán:
    "🆕NUEVO WEB"
    "👀VISTO"
    "✅PROCESADO"
""")
else:
    print("""
❌ NINGÚN FORMATO COINCIDE COMPLETAMENTE

Posibles causas:
1. Las opciones en Airtable tienen formato diferente
2. Hay caracteres especiales adicionales
3. Problema de encoding

Opciones reales en Airtable:
""")
    for idx, opcion in enumerate(opciones_reales, 1):
        print(f"   {idx}. \"{opcion}\"")
        print(f"      Bytes: {opcion.encode('utf-8')}")
        print(f"      Caracteres:")
        for i, char in enumerate(opcion):
            print(f"         [{i}] = '{char}' (U+{ord(char):04X})")
        print()

    print("""
Solución:
1. Copiar EXACTAMENTE una opción de arriba
2. Actualizar las constantes en backend/main.py
""")

# 6. Test adicional: leer registros existentes
print("\n" + "=" * 80)
print("🔎 VERIFICACIÓN ADICIONAL: Valores en registros reales")
print("=" * 80)

tabla_url = f"https://api.airtable.com/v0/{BASE_ID}/DENUNCIA DE ACCIDENTE"
params = {
    "filterByFormula": "NOT({ESTADO_WEB} = '')",
    "maxRecords": 3,
    "fields[]": ["ESTADO_WEB"]
}

response = requests.get(tabla_url, headers=headers, params=params)

if response.status_code == 200:
    records = response.json().get("records", [])

    if records:
        print(f"\n✅ Encontrados {len(records)} registros con ESTADO_WEB poblado:")

        for rec in records:
            valor = rec["fields"].get("ESTADO_WEB", "N/A")
            print(f"\n   Valor: \"{valor}\"")

            # Check match
            if valor in formatos["CON_ESPACIO"].values():
                print(f"   ✅ Match con formato CON ESPACIO")
            elif valor in formatos["SIN_ESPACIO"].values():
                print(f"   ✅ Match con formato SIN ESPACIO")
            else:
                print(f"   ❌ No hace match con ningún formato")
    else:
        print("\n⚠️  No se encontraron registros con ESTADO_WEB poblado")
        print("   (Esto es normal si nunca se llenó correctamente antes)")
else:
    print(f"\n⚠️  No se pudieron leer registros: {response.status_code}")

print("\n" + "=" * 80)
