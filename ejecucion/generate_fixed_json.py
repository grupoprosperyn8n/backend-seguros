import json
import os

# Paths
INPUT_FILE = "/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/backend/n8n_workflow_crear_siniestro.json"
OUTPUT_FILE = "/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/backend/n8n_workflow_crear_siniestro_FIXED.json"

# Correct JS Code
MAPEAR_DATOS_JS = r"""const webhookData = $('Webhook').first().json;
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

MERGE_CLIENTE_JS = r"""const prevData = $('Mapear Datos').first().json;
const payload = { ...prevData.airtablePayload };

try {
  const clienteRecords = $('Buscar Cliente DNI').first().json.records || [];
  if (clienteRecords.length > 0) {
    payload['CLIENTE'] = [clienteRecords[0].id];
  }
} catch(e) {}

return [{ json: { tablaDestino: prevData.tablaDestino, payload } }];"""

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: No se encuentra {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    # Buscar y corregir nodos
    corrected_count = 0
    nodes = data.get('nodes', [])
    for node in nodes:
        if node.get('name') == 'Mapear Datos':
            node['parameters']['jsCode'] = MAPEAR_DATOS_JS
            print("Variable MAPEAR_DATOS_JS inyectada correctamente.")
            corrected_count += 1
        elif node.get('name') == 'Merge Cliente':
            node['parameters']['jsCode'] = MERGE_CLIENTE_JS
            print("Variable MERGE_CLIENTE_JS inyectada correctamente.")
            corrected_count += 1

    if corrected_count == 0:
        print("Advertencia: No se encontraron los nodos 'Mapear Datos' o 'Merge Cliente' para corregir.")
    
    # Asegurar que el nombre sea distintivo
    data['name'] = "CREAR_SINIESTRO_DYNAMIC_FIXED"

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Archivo generado exitosamente: {OUTPUT_FILE}")
    print("Copia este contenido y pégalo en n8n (Import from File o Ctrl+V en el canvas).")

if __name__ == '__main__':
    main()
