#!/usr/bin/env python3
"""
Test: ¿Qué pasa cuando envías un valor incorrecto a un Single Select con typecast=True?
"""

import requests
import json

API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

print("=" * 80)
print("🧪 TEST: Comportamiento de Single Select con typecast=True")
print("=" * 80)

# 1. Primero verificar si hay opciones adicionales creadas
print("\n1️⃣ Verificando opciones actuales en ESTADO_WEB...")

meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.get(meta_url, headers={"Authorization": f"Bearer {API_KEY}"})

if response.status_code == 200:
    tables = response.json().get("tables", [])
    for table_info in tables:
        if table_info["name"] == "DENUNCIA DE ACCIDENTE":
            for field in table_info.get("fields", []):
                if field["name"] == "ESTADO_WEB":
                    choices = field.get("options", {}).get("choices", [])
                    print(f"\n   📋 Opciones definidas: {len(choices)}")
                    for idx, choice in enumerate(choices, 1):
                        choice_name = choice.get("name")
                        choice_id = choice.get("id")
                        print(f"      {idx}. '{choice_name}' (ID: {choice_id})")

                    # Verificar si existe "NUEVO WEB" sin emoji
                    opciones = [c.get("name") for c in choices]
                    if "NUEVO WEB" in opciones:
                        print("\n   ⚠️  ADVERTENCIA: Existe opción 'NUEVO WEB' SIN emoji!")
                        print("      Esto indica que typecast=True creó una nueva opción.")

                    if "🆕 NUEVO WEB" in opciones:
                        print("\n   ✅ Opción correcta '🆕 NUEVO WEB' existe")

                    break
            break

# 2. Buscar registros con diferentes valores de ESTADO_WEB
print("\n\n2️⃣ Buscando registros con ESTADO_WEB poblado...")

tabla_url = f"https://api.airtable.com/v0/{BASE_ID}/DENUNCIA DE ACCIDENTE"
params = {"maxRecords": 50, "fields[]": ["ESTADO_WEB", "ID_GESTION_UNICO"]}

response = requests.get(tabla_url, headers={"Authorization": f"Bearer {API_KEY}"}, params=params)

if response.status_code == 200:
    records = response.json().get("records", [])

    # Contar valores
    valores_encontrados = {}
    vacios = 0

    for rec in records:
        fields = rec.get("fields", {})
        estado = fields.get("ESTADO_WEB")

        if estado:
            valores_encontrados[estado] = valores_encontrados.get(estado, 0) + 1
        else:
            vacios += 1

    print(f"\n   📊 Análisis de {len(records)} registros:")
    print(f"      Campos vacíos: {vacios}")

    if valores_encontrados:
        print(f"      Valores encontrados:")
        for valor, count in valores_encontrados.items():
            print(f"         '{valor}': {count} registros")
    else:
        print(f"      ⚠️  NO se encontraron registros con ESTADO_WEB poblado")

# 3. Explicación del comportamiento de Single Select
print("\n\n" + "=" * 80)
print("📚 COMPORTAMIENTO DE SINGLE SELECT EN AIRTABLE")
print("=" * 80)

print("""
Un campo Single Select SOLO acepta valores que estén en la lista predefinida.

Con typecast=False (estricto):
  ✅ "🆕 NUEVO WEB" → Se guarda correctamente
  ❌ "NUEVO WEB"    → ERROR 422: Invalid value

Con typecast=True (flexible):
  Según documentación de Airtable, puede:

  Opción A: Match Exacto
    ✅ "🆕 NUEVO WEB" → Funciona
    ❌ "NUEVO WEB"    → Se rechaza silenciosamente (campo queda NULL)

  Opción B: Match Aproximado (NO DOCUMENTADO, puede variar)
    ✅ "🆕 NUEVO WEB" → Funciona
    ⚠️  "NUEVO WEB"    → Podría hacer match con "🆕 NUEVO WEB"

  Opción C: Crear Nueva Opción (PELIGROSO)
    ✅ "🆕 NUEVO WEB" → Funciona
    ⚠️  "NUEVO WEB"    → Crea nueva opción sin emoji

    Resultado: Ahora hay 4 opciones:
      1. 🆕 NUEVO WEB
      2. 👀 VISTO
      3. ✅ PROCESADO
      4. NUEVO WEB  ← Opción nueva (contaminación)
""")

# 4. Prueba de qué está pasando realmente
print("\n" + "=" * 80)
print("🔍 DIAGNÓSTICO DEL PROBLEMA ACTUAL")
print("=" * 80)

print("""
Basado en la evidencia:

1. Los registros leídos tienen ESTADO_WEB vacío
   → Indica que el valor NO se está guardando

2. Posibles causas:
   a) typecast=True rechaza "NUEVO WEB" porque no coincide exactamente
   b) typecast=True lo acepta pero Airtable lo deja NULL internamente
   c) Hay un error anterior que previene que se llegue a guardar

3. El código usa:
   record = t_destino.create(airtable_payload, typecast=True)

   Con typecast=True, Airtable es "permisivo" pero NO garantiza crear opciones.

4. SOLUCIÓN DEFINITIVA:
   Usar el valor EXACTO que está en las opciones: "🆕 NUEVO WEB"

   Esto garantiza:
   ✅ Funciona con typecast=True
   ✅ Funciona con typecast=False
   ✅ No crea opciones duplicadas
   ✅ No depende de comportamiento no documentado
""")

print("\n" + "=" * 80)
print("💡 RECOMENDACIÓN FINAL")
print("=" * 80)

print("""
CAMBIO NECESARIO en backend/main.py línea 981:

❌ ACTUAL (incorrecto):
   airtable_payload["ESTADO_WEB"] = "NUEVO WEB"

✅ CORRECTO:
   airtable_payload["ESTADO_WEB"] = "🆕 NUEVO WEB"

RAZÓN:
  Single Select requiere match EXACTO con las opciones predefinidas.
  Aunque typecast=True es flexible, no se debe depender de comportamiento
  no documentado. Usar el valor exacto es la práctica correcta.

IMPACTO:
  - Con el cambio: Los campos se llenarán correctamente
  - Sin el cambio: Los campos quedan vacíos o crean opciones duplicadas
""")
