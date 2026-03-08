"""
fix_n8n_workflow.py
Corrige los nodos Code del workflow CREAR_SINIESTRO_DYNAMIC en n8n.
El problema: al importar via clipboard, los \n se guardaron como texto literal.

Estrategia: Usar la API REST de n8n para:
1. Obtener el workflow actual
2. Reemplazar el jsCode de 'Mapear Datos' y 'Merge Cliente'
3. Guardar el workflow corregido
"""

import requests
import json
import sys

# === CONFIGURACIÓN ===
N8N_BASE = "https://primary-production-0abcf.up.railway.app"
N8N_EMAIL = "diegol@grupoprosper.com"
N8N_PASSWORD = "Prosperdigital2025"
WORKFLOW_ID = "ydhSaoymAgTBSAHK"

# === CÓDIGO JS CORRECTO ===

MAPEAR_DATOS_JS = """const webhookData = $('Webhook').first().json;
const tipoFormulario = webhookData.tipo_formulario;
const datos = webhookData.datos || {};
const archivos = webhookData.archivos || {};
const polizaRecordId = webhookData.poliza_record_id;
const dni = webhookData.dni;

const formularios = $('GET Config Formularios').first().json.records || [];
const formRecord = formularios.find(f => f.fields.CODIGO === tipoFormulario);

if (!formRecord) {
  return [{ json: { error: true, message: `Formulario '${tipoFormulario}' no encontrado` } }];
}

const formId = formRecord.id;
const tablaDestino = formRecord.fields['TABLA RELACIONADA'];

if (!tablaDestino) {
  return [{ json: { error: true, message: `Sin TABLA RELACIONADA para '${tipoFormulario}'` } }];
}

const campos = $('GET Config Campos').first().json.records || [];
const fieldMap = {};

campos.forEach(c => {
  const fields = c.fields;
  const linkedForms = fields.FORMULARIO || fields.Formulario || [];
  if (linkedForms.includes(formId)) {
    const idCampo = fields['ID CAMPO'];
    const columna = fields['COLUMNA AIRTABLE'];
    if (idCampo && columna) {
      fieldMap[idCampo] = columna;
    }
  }
});

const airtablePayload = {};

for (const [key, value] of Object.entries(datos)) {
  if (fieldMap[key] && value !== '' && value !== null && value !== undefined) {
    airtablePayload[fieldMap[key]] = value;
  }
}

for (const [key, urls] of Object.entries(archivos)) {
  if (fieldMap[key] && urls.length > 0) {
    airtablePayload[fieldMap[key]] = urls;
  }
}

if (polizaRecordId) {
  airtablePayload['POLIZAS'] = [polizaRecordId];
}

return [{ json: { tablaDestino, airtablePayload, dni, error: false } }];"""

MERGE_CLIENTE_JS = """const prevData = $('Mapear Datos').first().json;
const payload = { ...prevData.airtablePayload };

try {
  const clienteRecords = $('Buscar Cliente DNI').first().json.records || [];
  if (clienteRecords.length > 0) {
    payload['CLIENTE'] = [clienteRecords[0].id];
  }
} catch(e) {}

return [{ json: { tablaDestino: prevData.tablaDestino, payload } }];"""

def main():
    print("🔐 Autenticando en n8n...")
    
    # 1. Login
    session = requests.Session()
    login_resp = session.post(f"{N8N_BASE}/rest/login", json={
        "email": N8N_EMAIL,
        "password": N8N_PASSWORD
    })
    
    if login_resp.status_code != 200:
        print(f"❌ Login falló: {login_resp.status_code}")
        print(login_resp.text[:500])
        sys.exit(1)
    
    print("✅ Login exitoso")
    
    # 2. Obtener workflow actual
    print(f"📥 Obteniendo workflow {WORKFLOW_ID}...")
    wf_resp = session.get(f"{N8N_BASE}/rest/workflows/{WORKFLOW_ID}")
    
    if wf_resp.status_code != 200:
        print(f"❌ No se pudo obtener workflow: {wf_resp.status_code}")
        print(wf_resp.text[:500])
        sys.exit(1)
    
    wf_data = wf_resp.json()
    workflow = wf_data.get("data", wf_data)
    
    print(f"✅ Workflow obtenido: {workflow.get('name', 'sin nombre')}")
    print(f"   Nodos: {[n['name'] for n in workflow['nodes']]}")
    
    # 3. Corregir nodos Code
    fixed_count = 0
    
    for node in workflow['nodes']:
        if node['name'] == 'Mapear Datos':
            old_code = node['parameters'].get('jsCode', '')
            node['parameters']['jsCode'] = MAPEAR_DATOS_JS
            fixed_count += 1
            has_literal_newlines = '\\n' in old_code and '\n' not in old_code
            print(f"🔧 Mapear Datos: corregido (tenía \\n literales: {has_literal_newlines})")
            
        elif node['name'] == 'Merge Cliente':
            old_code = node['parameters'].get('jsCode', '')
            node['parameters']['jsCode'] = MERGE_CLIENTE_JS
            fixed_count += 1
            has_literal_newlines = '\\n' in old_code and '\n' not in old_code
            print(f"🔧 Merge Cliente: corregido (tenía \\n literales: {has_literal_newlines})")
    
    if fixed_count == 0:
        print("⚠️ No se encontraron nodos para corregir")
        sys.exit(1)
    
    # 4. Guardar workflow
    print(f"💾 Guardando workflow corregido...")
    
    save_resp = session.put(
        f"{N8N_BASE}/rest/workflows/{WORKFLOW_ID}",
        json=workflow,
        headers={"Content-Type": "application/json"}
    )
    
    if save_resp.status_code == 200:
        print("✅ Workflow guardado exitosamente")
    else:
        print(f"❌ Error al guardar: {save_resp.status_code}")
        print(save_resp.text[:500])
        sys.exit(1)
    
    # 5. Activar workflow
    print("🚀 Activando workflow...")
    activate_resp = session.patch(
        f"{N8N_BASE}/rest/workflows/{WORKFLOW_ID}",
        json={"active": True},
        headers={"Content-Type": "application/json"}
    )
    
    if activate_resp.status_code == 200:
        print("✅ Workflow activado")
    else:
        print(f"⚠️ Activación: {activate_resp.status_code}")
        print(activate_resp.text[:300])
    
    # 6. Verificar
    print("\n📋 Verificando workflow guardado...")
    verify_resp = session.get(f"{N8N_BASE}/rest/workflows/{WORKFLOW_ID}")
    if verify_resp.status_code == 200:
        verify_data = verify_resp.json()
        vw = verify_data.get("data", verify_data)
        for node in vw['nodes']:
            if node['name'] in ('Mapear Datos', 'Merge Cliente'):
                code = node['parameters'].get('jsCode', '')
                has_real_newlines = '\n' in code
                line_count = code.count('\n') + 1
                print(f"   {node['name']}: {line_count} líneas, newlines reales: {has_real_newlines}")
    
    print("\n🎉 ¡Workflow corregido y listo!")

if __name__ == "__main__":
    main()
