
import re

def parse_poliza_block(bloque_texto: str) -> dict:
    """
    Parsea un bloque de ETIQUETA_POLIZA y extrae toda la información.
    """
    
    info = {
        "numero": "",
        "patente": "",
        "tipo_vehiculo": "",
        "categoria": "",
        "vida": False,
        "auxilio": False,
        "estado": "",
        "descripcion_completa": bloque_texto.strip()
    }
    
    # Extraer N° POL (buscar patrón más flexible)
    match = re.search(r'N°\s*POL:?\s*(\d+)', bloque_texto, re.IGNORECASE)
    if match:
        info["numero"] = match.group(1)
    
    # Extraer Patente (después del emoji 🏷️)
    match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque_texto)
    if match:
        info["patente"] = match.group(1)
    
    # Extraer Tipo de vehículo (buscar palabra después de emoji de vehículo)
    match = re.search(r'[🚗🚙🚛🏍️]\s+([A-ZÁ-Ú]+)', bloque_texto)
    if match:
        info["tipo_vehiculo"] = match.group(1).strip()
    
    # Extraer Estado (Ej: VENCE 30D, VIGENTE, ANULADA)
    # Buscamos patrones comunes de estado
    if "ANULADA" in bloque_texto:
        info["estado"] = "ANULADA"
    elif "VENCE" in bloque_texto:
        match = re.search(r'(VENCE\s*\d+D?)', bloque_texto)
        if match:
            info["estado"] = match.group(1)
    elif "VIGENTE" in bloque_texto:
        info["estado"] = "VIGENTE"
        
    # Extraer Vida
    if "VIDA: SI" in bloque_texto or "❤️ VIDA" in bloque_texto:
        info["vida"] = True
        
    # Extraer Auxilio
    if "AUX" in bloque_texto or "🆘" in bloque_texto or "🔧" in bloque_texto:
        info["auxilio"] = True
        
    return info

# EL CASO REPORTADO EN LA SCREENSHOT (SIMULADO)
# Contiene multiples polizas concatenadas
raw_airtable_string = "✅ ⏳ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🆘 AUX ✅ VENCE 30D | ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"

print(f"STRING ORIGINAL: {raw_airtable_string}\n")

# LÓGICA ACTUAL EN MAIN.PY (Extracto simulado)
# El problema: main.py probablemente busca LA PRIMERA coincidencia global en el string completo
# en lugar de separar las pólizas primero.

input_patente = "PDL384"
print(f"BUSCANDO PATENTE: {input_patente}")

# Simulando lo que hace main.py actualmente (aprox)
# Probablemente divide por " | " pero si el string tiene multiples emojies de inicio, es un problema.
# Vamos a ver como dividir este string masivo en "bloques" reales.

# Intento 1: Split por salto de linea? No, parece que airtable rollups a veces usan coma com separator o nada.
# En la screenshot se ve todo seguido. Pero entre una poliza y otra hay un patron.
# Empieza con emojis de estado ✅, ⏳, 🔴, etc.

# Regex para splitear por el inicio de una nueva poliza (suponiendo que empiezan con indicadores de estado o emojis especificos)
# O quizas dividir por la patente buscada?

parsed = parse_poliza_block(raw_airtable_string)
print(f"\nPARSEO DIRECTO (Como lo hace main.py hoy):")
print(parsed)
print(f"¿Numero correcto? {parsed['numero'] == '33333333'}")

# PRUEBA 2: Imaginemos que dividimos el string por el separador de registros de Airtable.
# Usualmente es una coma "," si es un array lookup, pero si es un string rollup puede ser cualquier cosa.

list_from_airtable = ["✅ ⏳ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🆘 AUX", "✅ VENCE 30D | ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"]
# Si main.py recibe una lista (Lookup field), es facil.
# Si recibe un string (Rollup text), es dificil.
