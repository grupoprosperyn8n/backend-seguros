#!/usr/bin/env python3
"""
Script para verificar el comportamiento del campo ESTADO_WEB
Prueba si "NUEVO WEB" funciona o necesita el emoji "🆕 NUEVO WEB"
"""

from pyairtable import Api

# Credenciales
API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

api = Api(API_KEY)
base = api.base(BASE_ID)

# Probar con DENUNCIA DE ACCIDENTE primero
tabla = base.table("DENUNCIA DE ACCIDENTE")

print("=" * 80)
print("🧪 PRUEBA: Verificar comportamiento de ESTADO_WEB")
print("=" * 80)

# 1. Obtener un registro existente para ver las opciones reales
print("\n1️⃣ Leyendo registros existentes para ver valores de ESTADO_WEB...")
try:
    records = tabla.all(max_records=5, fields=["ESTADO_WEB", "ID_GESTION_UNICO"])

    if records:
        print(f"✅ Se encontraron {len(records)} registros\n")
        for rec in records:
            estado = rec['fields'].get('ESTADO_WEB', 'N/A')
            id_gestion = rec['fields'].get('ID_GESTION_UNICO', 'N/A')
            print(f"   ID: {id_gestion}")
            print(f"   ESTADO_WEB: '{estado}'")
            print(f"   Tipo: {type(estado)}")
            print(f"   Tiene emoji: {'🆕' in str(estado) or '👀' in str(estado) or '✅' in str(estado)}")
            print()
    else:
        print("⚠️ No se encontraron registros con ESTADO_WEB")

except Exception as e:
    print(f"❌ Error leyendo registros: {e}")

# 2. Intentar obtener el schema del campo
print("\n2️⃣ Intentando obtener schema del campo ESTADO_WEB...")
try:
    # Usar Meta API para obtener schema completo
    import requests

    meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(meta_url, headers=headers)
    if response.status_code == 200:
        tables = response.json().get("tables", [])

        for table_info in tables:
            if table_info["name"] == "DENUNCIA DE ACCIDENTE":
                for field in table_info.get("fields", []):
                    if field["name"] == "ESTADO_WEB":
                        print(f"✅ Campo encontrado!")
                        print(f"   Tipo: {field.get('type')}")

                        if field.get("type") == "singleSelect":
                            choices = field.get("options", {}).get("choices", [])
                            print(f"   Opciones definidas ({len(choices)}):")
                            for choice in choices:
                                choice_name = choice.get("name")
                                print(f"      - '{choice_name}'")
                                print(f"        * Bytes: {choice_name.encode('utf-8')}")
                                print(f"        * Length: {len(choice_name)}")
                        break
                break
    else:
        print(f"⚠️ No se pudo obtener schema: {response.status_code}")

except Exception as e:
    print(f"❌ Error obteniendo schema: {e}")

# 3. Prueba de escritura (comentada por seguridad)
print("\n3️⃣ Análisis de compatibilidad:")
print("\n   📝 Valores que el backend intenta escribir:")
print("      Backend:  'NUEVO WEB'")
print("\n   🎯 Valores esperados por Airtable:")
print("      Opción 1: '🆕 NUEVO WEB'")
print("      Opción 2: '👀 VISTO'")
print("      Opción 3: '✅ PROCESADO'")

print("\n   🔍 Comparación:")
backend_value = "NUEVO WEB"
airtable_value = "🆕 NUEVO WEB"

print(f"      ¿Son iguales? {backend_value == airtable_value}")
print(f"      ¿Backend está en Airtable? {backend_value in airtable_value}")
print(f"      Diferencia: '{airtable_value}' tiene emoji '🆕' al inicio")

print("\n" + "=" * 80)
print("📊 CONCLUSIÓN:")
print("=" * 80)

print("""
Si Airtable usa match estricto:
  ❌ Backend falla porque "NUEVO WEB" != "🆕 NUEVO WEB"

Si Airtable usa match con typecast=True:
  ✅ Puede funcionar si ignora emojis
  ⚠️  O crea nueva opción sin emoji (contaminación de datos)

RECOMENDACIÓN:
  Cambiar línea 981 de main.py a:
  airtable_payload["ESTADO_WEB"] = "🆕 NUEVO WEB"
""")

print("\n💡 Para probar escritura real (descomentado):")
print("   Descomentar sección 4 del script")
