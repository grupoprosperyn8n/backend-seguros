
import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def fix_config_campos():
    t_campos = Table(API_KEY, BASE_ID, "CONFIG_CAMPOS")
    
    # 1. Obtener todos los campos de configuración
    records = t_campos.all()
    print(f"Buscando campos para corregir en {len(records)} registros...")
    
    # Mapeo de correcciones necesarias detectadas en la inspección
    correcciones = {
        "f_relato": "RELATOS DEL HECHO",
        "f_fecha": "FECHA DEL SINIESTRO",
        "f_hora": "HORA APROX. DEL SINIESTRO",
        "f_lugar": "DIRECCIÓN Y N°",
        "f_localidad": "LUGAR O ESTABLECIMIENTO"
    }
    
    actualizados = 0
    for r in records:
        id_campo = r["fields"].get("ID CAMPO")
        if id_campo in correcciones:
            nuevo_valor = correcciones[id_campo]
            valor_actual = r["fields"].get("COLUMNA AIRTABLE")
            
            if valor_actual != nuevo_valor:
                print(f"🔧 Corrigiendo {id_campo}: '{valor_actual}' -> '{nuevo_valor}'")
                t_campos.update(r["id"], {"COLUMNA AIRTABLE": nuevo_valor})
                actualizados += 1
    
    print(f"✅ Proceso terminado. Se actualizaron {actualizados} registros.")

if __name__ == "__main__":
    fix_config_campos()
