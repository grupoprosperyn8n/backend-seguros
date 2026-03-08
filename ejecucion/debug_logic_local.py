
import re

def parse_poliza_block(bloque_texto: str) -> list:
    import re
    if not bloque_texto: return []
    # Regex ajustado sin escapes problematicos
    SEPARATORS_PATTERN = r'(?=[✅🔴🟢⏳⚠️❌])' 
    posibles_bloques = re.split(SEPARATORS_PATTERN, bloque_texto)
    bloques = [b.strip() for b in posibles_bloques if b.strip()]
    if not bloques: bloques = [bloque_texto]
    parsed_policies = []
    
    print(f"DEBUG: Texto entrada: {bloque_texto}")
    print(f"DEBUG: Bloques split: {bloques}")

    for bloque in bloques:
        p_info = {"numero": "", "patente": "", "tipo_vehiculo": "", "categoria": "", "vida": False, "auxilio": False, "estado": "", "descripcion_completa": bloque}
        match = re.search(r'N[°][ ]*POL[:]?[ ]*([0-9]+)', bloque, re.IGNORECASE)
        if not match: match = re.search(r'([0-9]{5,})', bloque)
        if match: p_info["numero"] = match.group(1)
        
        match = re.search(r'🏷️[ ]*([A-Z0-9]+)', bloque, re.IGNORECASE)
        if not match: match = re.search(r'([A-Z]{2,3}[0-9]{3}[A-Z]{0,2})', bloque)
        if match: p_info["patente"] = match.group(1).upper()
        
        parsed_policies.append(p_info)
        print(f"DEBUG: Parsed Poliza: {p_info}")

    return parsed_policies

def validate_siniestro_mock(dni, patente, etiqueta_raw):
    dni_limpio = "".join(filter(str.isdigit, str(dni)))
    patente_limpia = patente.upper().strip().replace(" ", "")
    
    compilacion = etiqueta_raw
    if isinstance(compilacion, list):
        texto_polizas = " | ".join([str(x) for x in compilacion])
    else:
        texto_polizas = str(compilacion or "")

    print(f"DEBUG: Patente limpia: '{patente_limpia}'")
    print(f"DEBUG: Texto Polizas: '{texto_polizas.upper()}'")

    if patente_limpia not in texto_polizas.upper():
        print("❌ FAIL: Patente no encontrada en texto (check simple)")
        return
    else:
        print("✅ PASS: Patente encontrada en texto (check simple)")

    # Lógica de bloques
    parts = [p.strip() for p in texto_polizas.split("|")]
    bloques_detectados = []
    current_bloque = []
    emojis_inicio = ["✅", "❌", "⏳", "⚠️"]
    
    for part in parts:
        es_inicio = any(e in part for e in emojis_inicio) and ("VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part or "SIN VIGENCIA" in part) # Ojo: agregué SIN VIGENCIA aqui para testear si mi logica original estaba mal
        # Logica original NO tenia "SIN VIGENCIA" en el OR.
        # Original: ("VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part)
        
        # Vou a usar la logica EXACTA de main.py
        es_inicio_main = any(e in part for e in emojis_inicio) and ("VENCE" in part or "ANULADA" in part or "BAJA" in part or "ACTIVA" in part)
        
        if not current_bloque:
            current_bloque.append(part)
        elif es_inicio_main:
            bloques_detectados.append(" | ".join(current_bloque))
            current_bloque = [part]
        else:
            current_bloque.append(part)
            
    if current_bloque:
        bloques_detectados.append(" | ".join(current_bloque))

    bloque_match = None
    for bloque in bloques_detectados:
        if patente_limpia in bloque.upper():
            bloque_match = bloque
            break
            
    if not bloque_match:
        bloque_match = texto_polizas
        
    print(f"DEBUG: Bloque Match: {bloque_match}")

    parsed_list = parse_poliza_block(bloque_match)
    poliza_info = parsed_list[0] if parsed_list else {}
    print(f"RESULTADO FINAL: {poliza_info}")

# DATOS REALES (DNI 43770731)
etiqueta_real = "✅  🟣 SIN VIGENCIA   |   🚗 AUTO   |   N° POL: 3455666   |   🏷️ 234RTY   |   🛡️ B4   |   🆘 AUX 300"
validate_siniestro_mock("43770731", "234RTY", etiqueta_real)
