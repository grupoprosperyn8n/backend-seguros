
import re

raw_string = "✅ ⏳ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🆘 AUX  ✅ VENCE 30D | ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"

# Pattern: Split before any of the common status emojis
# We filter empty strings resulting from the split at the start
blocks = re.split(r'(?=[✅🔴🟢⏳])', raw_string)
blocks = [b.strip() for b in blocks if b.strip()]

print(f"ENCONTRADOS {len(blocks)} BLOQUES:")
for i, b in enumerate(blocks):
    print(f"BLOQUE {i+1}: {b}")
    
# Parsing functio adapted
def parse_block(bloque):
    info = {}
    match_patente = re.search(r'🏷️\s*([A-Z0-9]+)', bloque)
    if match_patente:
        info['patente'] = match_patente.group(1)
        
    match_num = re.search(r'N°\s*POL:?\s*(\d+)', bloque)
    if match_num:
        info['numero'] = match_num.group(1)
        
    if "ANULADA" in bloque:
        info['estado'] = "ANULADA"
    elif "VIGENTE" in bloque:
        info['estado'] = "VIGENTE"
    elif "VENCE" in bloque:
        info['estado'] = "VENCE PRONTO"
        
    return info

print("\nRESULTADOS POR BLOQUE:")
target_patente = "PDL384"
for b in blocks:
    p = parse_block(b)
    print(p)
    if p.get('patente') == target_patente:
        print(f"✅ MATCH CORRECTO PARA {target_patente}: {p}")
