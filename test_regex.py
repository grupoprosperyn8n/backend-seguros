import re

def parse_poliza_block(text: str):
    polizas = []
    
    # 1. Split por iconos de estado
    blocks = re.split(r'(?=[✅⏳❌🟢🔴🟡🟣⭕⚪])', text)
    
    for block in blocks:
        if not block.strip():
            continue
            
        p = {
            "estado": "Desconocido",
            "tipo_vehiculo": "Vehículo",
            "numero": "",
            "patente": "",
            "cobertura": "",
            "vida": "",
            "auxilio": "",
            "descripcion_completa": block.strip()
        }
        
        # Patrón para número de póliza
        num_m = re.search(r'N° POL:\s*([A-Za-z0-9-]+)', block)
        if num_m:
            p["numero"] = num_m.group(1).strip()
            
        # Patrón para patente
        pat_m = re.search(r'🏷️\s*([A-Z0-9 ]+?)\s*\|', block)
        if pat_m:
            # Eliminar todos los espacios de la patente extraída
            p["patente"] = pat_m.group(1).replace(" ", "").upper()
        else:
            # Fallback patente
            fall_m = re.search(r'([A-Z]{2,3}\s*\d{3}[A-Z]{0,2})', block)
            if fall_m:
                p["patente"] = fall_m.group(1).replace(" ", "").upper()
                
        polizas.append(p)
        
    return polizas

text = "✅  🟣 SIN VIGENCIA   |   🚗 AUTO   |   N° POL: 3455666   |   🏷️ 234RTY   |   🛡️ B4   |   🆘 AUX 300"
res = parse_poliza_block(text)
print(res)
