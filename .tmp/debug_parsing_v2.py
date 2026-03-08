import re

def parse_poliza_block(bloque_texto: str) -> list:
    if not bloque_texto:
        return []

    # Expresión regular para separar por emojis de estado (inicio de bloque)
    # Buscamos emojis de estado seguidos de texto
    SEPARATORS_PATTERN = r'(?=[✅🔴🟢⏳⚠️❌])' 
    posibles_bloques = re.split(SEPARATORS_PATTERN, bloque_texto)
    bloques = [b.strip() for b in posibles_bloques if b.strip()]

    if not bloques:
        bloques = [bloque_texto]

    parsed_policies = []
    
    for bloque in bloques:
        p_info = {
            "numero": "",
            "patente": "",
            "tipo_vehiculo": "",
            "categoria": "",
            "vida": False,
            "auxilio": False,
            "estado": "",
            "descripcion_completa": bloque
        }
        
        # 1. N° Póliza
        match = re.search(r'N°\s*POL:?\s*(\d+)', bloque, re.IGNORECASE)
        if match:
            p_info["numero"] = match.group(1)
        
        # 2. Patente
        match = re.search(r'🏷️\s*([A-Z0-9]+)', bloque, re.IGNORECASE)
        if match:
            p_info["patente"] = match.group(1).upper()
        
        # 3. Tipo Vehículo
        match = re.search(r'[🚗🚙🚛🏍️]\s+([A-ZÁ-Ú]+)', bloque)
        if match:
            tipo = match.group(1).strip()
            if len(tipo) > 2 and tipo not in ["POL"]: 
                p_info["tipo_vehiculo"] = tipo
            
        # 4. Estado
        # Prioridad: ANULADA > VIGENTE > VENCE XD
        if "ANULADA" in bloque:
            p_info["estado"] = "ANULADA"
        elif "VIGENTE" in bloque:
            p_info["estado"] = "VIGENTE"
        
        # Caso VENCE 30D (sin VIGENTE explicito a veces)
        match_vence = re.search(r'(VENCE\s*\d+D?)', bloque)
        if match_vence:
            p_info["estado"] = match_vence.group(1)
        
        # 5. Vida y Aux
        if "VIDA: SI" in bloque or "❤️ VIDA" in bloque:
            p_info["vida"] = True
        if "AUX" in bloque or "🆘" in bloque or "🔧" in bloque:
            p_info["auxilio"] = True
            
        parsed_policies.append(p_info)

    return parsed_policies

# Test Case based on screenshot input
input_text = "✅ ⏳ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🛡️ A | ❤️ VIDA: SI | 🆘 AUX ✅ 🔴 ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"
input_text_2 = "✅ 🆘 AUX INFINITY ⏰ VENCE 7D | 🚗 TAXI | N° POL: 78546 | 🏷️ KHU789 | ❤️ VIDA"

print("--- TEST 1 ---")
results = parse_poliza_block(input_text)
for r in results:
    print(r)

print("\n--- TEST 2 (From User Screenshot) ---")
results2 = parse_poliza_block(input_text_2)
for r in results2:
    print(r)
