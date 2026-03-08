#!/usr/bin/env python3
"""
TEST DEFINITIVO: Probar AMBOS formatos (con y sin espacio)
para ver cuál funciona con el Single Select de Airtable
"""

import requests
import json

API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("🧪 TEST DEFINITIVO: Formato con y sin espacio")
print("=" * 80)

# Preparar 2 payloads de prueba
test_cases = [
    {
        "nombre": "CON ESPACIO",
        "valor": "🆕 NUEVO WEB",  # Con espacio
        "descripcion": "Emoji + espacio + texto"
    },
    {
        "nombre": "SIN ESPACIO",
        "valor": "🆕NUEVO WEB",   # Sin espacio
        "descripcion": "Emoji pegado al texto"
    }
]

print("\n📋 Formatos a probar:")
for idx, test in enumerate(test_cases, 1):
    print(f"\n{idx}. {test['nombre']}")
    print(f"   Valor: \"{test['valor']}\"")
    print(f"   Bytes: {test['valor'].encode('utf-8')}")
    print(f"   Caracteres:")
    for i, char in enumerate(test['valor']):
        print(f"      [{i}] = '{char}' (U+{ord(char):04X})", end="")
        if char == ' ':
            print(" ← ESPACIO")
        else:
            print()

# IMPORTANTE: NO vamos a crear registros reales
# Solo mostrar qué pasaría
print("\n\n" + "=" * 80)
print("📊 ANÁLISIS (sin crear registros)")
print("=" * 80)

print("""
Basado en los registros REALES leídos de Airtable:
- Todos tienen ESPACIO después del emoji
- Formato almacenado: "🆕 NUEVO WEB" (con U+0020)

Pero si visualmente en Airtable se ve pegado, puede ser:
1. Rendering de la interfaz (el navegador junta el emoji con texto)
2. La fuente usada hace que se vea sin espacio
3. Configuración regional/local

COMPORTAMIENTO DE SINGLE SELECT:
- Acepta el valor tal como está definido en las opciones
- Si envías "🆕NUEVO WEB" (sin espacio) y la opción es "🆕 NUEVO WEB" (con espacio)
  → NO hay match → Campo queda NULL

- Si envías "🆕 NUEVO WEB" (con espacio) y la opción es "🆕 NUEVO WEB" (con espacio)
  → HAY match → Campo se llena correctamente
""")

print("\n" + "=" * 80)
print("💡 RECOMENDACIÓN BASADA EN DATOS REALES")
print("=" * 80)

print("""
Los registros EXISTENTES en Airtable que SÍ tienen el campo poblado usan:
    "🆕 NUEVO WEB" (CON ESPACIO)

Por lo tanto, el backend debe enviar:
    EstadoWeb.NUEVO_WEB = "🆕 NUEVO WEB"  # Con espacio

Si después de implementar esto NO funciona, entonces:
1. Verificar las opciones directamente en Airtable UI
2. Copiar y pegar el valor EXACTO desde Airtable
3. O cambiar las opciones en Airtable para que coincidan
""")

# Leer las opciones EXACTAS una vez más del API
print("\n" + "=" * 80)
print("🔍 VERIFICACIÓN FINAL: Opciones del campo")
print("=" * 80)

meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.get(meta_url, headers={"Authorization": f"Bearer {API_KEY}"})

if response.status_code == 200:
    tables = response.json().get("tables", [])
    for table in tables:
        if table["name"] == "DENUNCIA DE ACCIDENTE":
            for field in table.get("fields", []):
                if field["name"] == "ESTADO_WEB":
                    choices = field.get("options", {}).get("choices", [])

                    print(f"\nOpciones definidas en el campo ESTADO_WEB:")
                    for idx, choice in enumerate(choices, 1):
                        name = choice.get("name")
                        print(f"\n{idx}. \"{name}\"")

                        # Test match
                        match_con = (name == "🆕 NUEVO WEB")
                        match_sin = (name == "🆕NUEVO WEB")

                        print(f"   ¿Match CON espacio? {match_con}")
                        print(f"   ¿Match SIN espacio? {match_sin}")

                        if match_con:
                            print(f"   ✅ USAR: EstadoWeb.NUEVO_WEB = \"{name}\"")
                        elif match_sin:
                            print(f"   ✅ USAR: EstadoWeb.NUEVO_WEB = \"{name}\"")
                    break
            break

print("\n" + "=" * 80)
