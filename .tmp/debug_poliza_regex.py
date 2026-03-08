
import re

def test_split(texto_polizas):
    print(f"\n--- Texto Original ---\n{texto_polizas}\n")
    
    # Intento 1: Regex original
    bloques_poliza = re.split(r'(?=[✅⏳❌⚠️])', texto_polizas)
    print(f"--- Regex Split (len={len(bloques_poliza)}) ---")
    for i, b in enumerate(bloques_poliza):
        print(f"[{i}] {b.strip()}")

    # Intento 2: Tokenizer approach
    tokens = [t.strip() for t in texto_polizas.split("|")]
    bloques = []
    current_bloque = []
    
    for token in tokens:
        # Check if token starts with a status emoji
        is_start = any(token.startswith(e) for e in ["✅", "⏳", "❌", "⚠️"])
        
        if is_start:
            if current_bloque:
                bloques.append(" | ".join(current_bloque))
            current_bloque = [token]
        else:
            current_bloque.append(token)
            
    if current_bloque:
        bloques.append(" | ".join(current_bloque))
        
    print(f"\n--- Tokenizer Split (len={len(bloques)}) ---")
    for i, b in enumerate(bloques):
        print(f"[{i}] {b}")

# Caso Real (Simulado)
texto = "✅ VENCE 30D | 🚗 AUTO | N° POL: 33333333 | 🏷️ PDL384 | 🅰️ A | ❤️ VIDA: SI | 🔧 AUX | ❌ ANULADA | 🚗 CAMIONETA | N° POL: 777742 | 🏷️ POL432"
test_split(texto)

# Caso Sin Espacios
texto2 = "✅VENCE 30D|🚗AUTO|N° POL:33333333|🏷️PDL384|❌ANULADA|🚗CAMIONETA|N° POL:777742|🏷️POL432"
test_split(texto2)
