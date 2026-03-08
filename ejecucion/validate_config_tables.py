import os
import sys
from pyairtable import Api

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Try to import config if possible, else hardcode for safety
try:
    from backend.main import BASE_ID, TABLE_FORMS, TABLE_FIELDS, API_KEY
except:
    API_KEY = "patXXX_REMOVED_XXX"
    BASE_ID = "appuhslj3GFf60Tea"
    TABLE_FORMS = "CONFIG_FORMULARIOS"
    TABLE_FIELDS = "CONFIG_CAMPOS"

def validate_tables():
    print("🕵️‍♂️ Iniciando Validación de Tablas de Configuración...")
    api = Api(API_KEY)
    t_forms = api.table(BASE_ID, TABLE_FORMS)
    t_fields = api.table(BASE_ID, TABLE_FIELDS)
    
    try:
        forms = t_forms.all()
        fields = t_fields.all()
    except Exception as e:
        print(f"❌ Error conectando a Airtable: {e}")
        return

    print(f"✅ Conexión Exitosa.")
    print(f"📊 Formularios encontrados: {len(forms)}")
    print(f"📊 Campos encontrados: {len(fields)}")
    
    # Validar Formularios
    print("\n--- 📝 Validación de Formularios ---")
    form_ids = {}
    for f in forms:
        codigo = f["fields"].get("CODIGO", "SIN CODIGO")
        title = f["fields"].get("TITULO", "SIN TITULO")
        target = f["fields"].get("TABLA RELACIONADA", "⚠️ NO DEFINIDO (Usará Fallback)")
        print(f"  • [{codigo}] {title} -> Destino: {target}")
        form_ids[f["id"]] = codigo
        
        # Check forbidden field
        if "Configuracion" in f["fields"]:
            print(f"    ⚠️ AVISO: El campo 'Configuracion' tiene datos (Ignorar, es legacy).")

    # Validar Campos
    print("\n--- 🧩 Validación de Campos ---")
    orphans = 0
    for c in fields:
        fid = c["fields"].get("ID CAMPO", "SIN ID")
        label = c["fields"].get("ETIQUETA", "SIN ETIQUETA")
        linked = c["fields"].get("Formulario", [])
        
        if not linked:
            print(f"    ❌ CAMPO HUÉRFANO: {fid} ({label}) - No tiene formulario asignado.")
            orphans += 1
        else:
            parent_id = linked[0]
            if parent_id not in form_ids:
                print(f"    ❌ ENLACE ROTO: {fid} apunta a un formulario inexistente ({parent_id})")
            # else:
            #     print(f"    ✅ {fid} -> {form_ids[parent_id]}")

    if orphans == 0:
        print("✅ Todos los campos están vinculados correctamente.")
    else:
        print(f"⚠️ Se encontraron {orphans} campos sin vincular.")

    print("\n🏁 Validación Finalizada.")

if __name__ == "__main__":
    validate_tables()
