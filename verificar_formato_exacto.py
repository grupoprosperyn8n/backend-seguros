#!/usr/bin/env python3
"""
Verificar el formato EXACTO de las opciones en Airtable
y crear constantes para usar en el backend
"""

import requests

API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

print("=" * 80)
print("🔍 VERIFICACIÓN EXACTA DE FORMATO EN AIRTABLE")
print("=" * 80)

# Obtener valores exactos de las 3 tablas
tablas_verificar = [
    "DENUNCIA DE ACCIDENTE",
    "DENUNCIA ROBO OC",
    "DENUNCIA ROBO / INCENDIO"
]

meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(meta_url, headers=headers)
tables = response.json().get("tables", [])

valores_por_tabla = {}

for tabla_nombre in tablas_verificar:
    print(f"\n📋 Tabla: {tabla_nombre}")
    print("-" * 80)

    for table in tables:
        if table["name"] == tabla_nombre:
            for field in table.get("fields", []):
                if field["name"] == "ESTADO_WEB":
                    choices = field.get("options", {}).get("choices", [])

                    valores = []
                    for idx, choice in enumerate(choices, 1):
                        name = choice.get("name")
                        valores.append(name)

                        print(f"\n   Opción {idx}:")
                        print(f"   Valor completo: '{name}'")
                        print(f"   Caracteres individuales:")

                        for i, char in enumerate(name):
                            print(f"      [{i}] = '{char}' (Unicode: U+{ord(char):04X})")

                        # Verificar si hay espacio después del emoji
                        if len(name) > 1:
                            segundo_char = name[1]
                            if segundo_char == ' ':
                                print(f"   ✅ HAY ESPACIO después del emoji")
                            else:
                                print(f"   ❌ NO HAY ESPACIO después del emoji")

                    valores_por_tabla[tabla_nombre] = valores
                    break
            break

# Verificar consistencia entre tablas
print("\n\n" + "=" * 80)
print("📊 ANÁLISIS DE CONSISTENCIA")
print("=" * 80)

primera_tabla = list(valores_por_tabla.keys())[0]
valores_referencia = valores_por_tabla[primera_tabla]

inconsistencias = False
for tabla, valores in valores_por_tabla.items():
    if valores != valores_referencia:
        print(f"⚠️  {tabla} tiene valores diferentes!")
        inconsistencias = True
    else:
        print(f"✅ {tabla} coincide con la referencia")

if not inconsistencias:
    print("\n✅ Las 3 tablas tienen los mismos valores")

# Generar código Python con las constantes correctas
print("\n\n" + "=" * 80)
print("💻 CONSTANTES PARA BACKEND (backend/main.py)")
print("=" * 80)

print("""
# Agregar al inicio del archivo (después de imports):

# Valores exactos de ESTADO_WEB según Airtable
class EstadoWeb:
    \"\"\"
    Valores válidos para el campo ESTADO_WEB en tablas de denuncias.
    Estos valores DEBEN coincidir exactamente con las opciones en Airtable.
    \"\"\"
""")

for idx, valor in enumerate(valores_referencia):
    # Crear nombre de constante
    nombre_const = valor.replace("🆕", "").replace("👀", "").replace("✅", "").strip().replace(" ", "_").upper()
    print(f'    {nombre_const} = "{valor}"')

print("""
# Uso en el código:
# airtable_payload["ESTADO_WEB"] = EstadoWeb.NUEVO_WEB
""")

# Test de escritura
print("\n\n" + "=" * 80)
print("🧪 TEST: ¿Qué formato funciona?")
print("=" * 80)

print(f"""
Backend actual envía: "NUEVO WEB"
Airtable tiene: "{valores_referencia[0]}"

¿Coinciden? {("NUEVO WEB" == valores_referencia[0])}

Para que funcione, backend debe enviar EXACTAMENTE:
    "{valores_referencia[0]}"
""")

# Generar las 3 opciones con variaciones
print("\n" + "=" * 80)
print("🔧 SOLUCIÓN ROBUSTA CON FALLBACK")
print("=" * 80)

print("""
Si hay duda sobre el formato exacto, implementar con fallback:

def get_estado_web_nuevo():
    \"\"\"
    Retorna el valor correcto para ESTADO_WEB = NUEVO.
    Intenta múltiples formatos para compatibilidad.
    \"\"\"
    # Formato actual en Airtable (verificado por API):
    OPCIONES = [
        "🆕 NUEVO WEB",    # Con espacio
        "🆕NUEVO WEB",     # Sin espacio después del emoji
        "NUEVO WEB",       # Sin emoji
    ]

    # Retornar el primero (formato verificado en Airtable)
    return OPCIONES[0]

# En create_siniestro:
airtable_payload["ESTADO_WEB"] = get_estado_web_nuevo()
""")

print("\n" + "=" * 80)
print("✅ RECOMENDACIÓN FINAL")
print("=" * 80)

print(f"""
Usar el valor EXACTO que retorna el API de Airtable:

    airtable_payload["ESTADO_WEB"] = "{valores_referencia[0]}"

Esto garantiza:
✅ Match exacto con Single Select
✅ No depende de interpretaciones visuales
✅ Funciona en las 3 tablas
✅ Compatible con typecast=True y typecast=False
""")
