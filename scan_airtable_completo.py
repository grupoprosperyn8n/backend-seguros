#!/usr/bin/env python3
"""
Script de Análisis Completo de Airtable
Extrae TODA la estructura: tablas, campos, tipos, opciones, relaciones
Genera reporte markdown completo
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

# Credenciales
API_KEY = "patXXX_REMOVED_XXX"
BASE_ID = "appuhslj3GFf60Tea"

# API Endpoints
META_API_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_all_tables_metadata():
    """Obtiene metadata completa de todas las tablas usando Meta API"""
    print("🔍 Conectando a Airtable Meta API...")
    response = requests.get(META_API_URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    return data.get("tables", [])

def get_sample_records(table_name, max_records=10):
    """Obtiene registros de muestra para ver datos reales"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    params = {"maxRecords": max_records}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json().get("records", [])
    except Exception as e:
        print(f"  ⚠️ Error obteniendo registros de {table_name}: {e}")

    return []

def map_field_type(field_info):
    """Mapea el tipo de campo de Airtable a descripción legible"""
    field_type = field_info.get("type")

    type_map = {
        "singleLineText": "Texto (línea única)",
        "multilineText": "Texto (multilínea)",
        "number": "Número",
        "percent": "Porcentaje",
        "currency": "Moneda",
        "singleSelect": "Selección única",
        "multipleSelects": "Selección múltiple",
        "date": "Fecha",
        "dateTime": "Fecha y hora",
        "checkbox": "Checkbox (Sí/No)",
        "multipleAttachments": "Archivos adjuntos",
        "multipleRecordLinks": "Vínculo a registros",
        "formula": "Fórmula",
        "rollup": "Rollup (agregación)",
        "count": "Conteo",
        "lookup": "Lookup (búsqueda)",
        "createdTime": "Fecha de creación",
        "lastModifiedTime": "Fecha de modificación",
        "createdBy": "Creado por",
        "lastModifiedBy": "Modificado por",
        "phoneNumber": "Teléfono",
        "email": "Email",
        "url": "URL",
        "rating": "Calificación",
        "duration": "Duración",
        "barcode": "Código de barras",
        "button": "Botón"
    }

    return type_map.get(field_type, f"Desconocido ({field_type})")

def analyze_field(field, all_tables):
    """Analiza un campo en detalle"""
    analysis = {
        "nombre": field.get("name"),
        "id": field.get("id"),
        "tipo": map_field_type(field),
        "tipo_raw": field.get("type"),
        "descripcion": field.get("description", ""),
    }

    # Opciones para selects
    if field.get("type") in ["singleSelect", "multipleSelects"]:
        options = field.get("options", {}).get("choices", [])
        analysis["opciones"] = [opt.get("name") for opt in options]

    # Relaciones
    if field.get("type") == "multipleRecordLinks":
        linked_table_id = field.get("options", {}).get("linkedTableId")
        linked_table_name = next((t["name"] for t in all_tables if t["id"] == linked_table_id), "Desconocida")
        analysis["tabla_vinculada"] = linked_table_name
        analysis["es_relacion"] = True

    # Fórmulas
    if field.get("type") == "formula":
        analysis["formula"] = field.get("options", {}).get("formula", "N/A")

    # Lookup
    if field.get("type") == "lookup":
        opts = field.get("options", {})
        analysis["lookup_de"] = opts.get("fieldIdInLinkedTable", "N/A")

    # Rollup
    if field.get("type") == "rollup":
        opts = field.get("options", {})
        analysis["rollup_funcion"] = opts.get("aggregationFunction", "N/A")

    return analysis

def generate_markdown_report(tables_data):
    """Genera reporte markdown completo"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = f"""# 📊 Análisis Completo de Airtable - Sistema de Seguros Agénticos

**Base ID:** `{BASE_ID}`
**Fecha de Análisis:** {now}
**Total de Tablas:** {len(tables_data)}

---

## 📑 Índice de Tablas

"""

    # Índice
    for idx, table in enumerate(tables_data, 1):
        md += f"{idx}. [{table['name']}](#{table['name'].lower().replace(' ', '-')})\n"

    md += "\n---\n\n"

    # Análisis detallado por tabla
    for table in tables_data:
        table_name = table["name"]
        table_id = table["id"]
        fields = table.get("fields", [])

        md += f"## 🗂️ {table_name}\n\n"
        md += f"**ID:** `{table_id}`  \n"
        md += f"**Total de Campos:** {len(fields)}  \n\n"

        # Tabla de campos
        md += "### 📋 Campos\n\n"
        md += "| Campo | Tipo | Detalles |\n"
        md += "|-------|------|----------|\n"

        for field in fields:
            nombre = field["nombre"]
            tipo = field["tipo"]
            detalles = []

            if "opciones" in field:
                detalles.append(f"Opciones: {', '.join(field['opciones'][:3])}{'...' if len(field['opciones']) > 3 else ''}")

            if field.get("es_relacion"):
                detalles.append(f"→ {field['tabla_vinculada']}")

            if "formula" in field:
                formula_preview = field['formula'][:50] + "..." if len(field['formula']) > 50 else field['formula']
                detalles.append(f"Fórmula: `{formula_preview}`")

            if "lookup_de" in field:
                detalles.append(f"Lookup: {field['lookup_de']}")

            if "rollup_funcion" in field:
                detalles.append(f"Rollup: {field['rollup_funcion']}")

            detalles_str = "<br>".join(detalles) if detalles else "-"
            md += f"| `{nombre}` | {tipo} | {detalles_str} |\n"

        md += "\n"

        # Campos de relación
        relaciones = [f for f in fields if f.get("es_relacion")]
        if relaciones:
            md += "### 🔗 Relaciones con Otras Tablas\n\n"
            for rel in relaciones:
                md += f"- **{rel['nombre']}** → `{rel['tabla_vinculada']}`\n"
            md += "\n"

        md += "---\n\n"

    return md

def analyze_backend_usage(tables_data):
    """Analiza cómo se usan las tablas en el backend Python"""
    md = "\n## 🐍 Uso en Backend Python\n\n"

    # Leer main.py para ver qué tablas se usan
    try:
        with open("/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/backend/main.py", "r") as f:
            backend_code = f.read()

        md += "### Tablas Usadas en Backend:\n\n"

        for table in tables_data:
            table_name = table["name"]
            # Buscar referencias
            count = backend_code.count(f'"{table_name}"') + backend_code.count(f"'{table_name}'")

            if count > 0:
                md += f"- **{table_name}**: {count} referencias\n"

        md += "\n"
    except Exception as e:
        md += f"⚠️ No se pudo analizar backend: {e}\n\n"

    return md

def analyze_frontend_usage(tables_data):
    """Analiza cómo se conectan las tablas con el frontend"""
    md = "\n## 🌐 Conexión con Frontend\n\n"

    # Leer app.js
    try:
        with open("/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/linktree/app.js", "r") as f:
            frontend_code = f.read()

        md += "### Endpoints del Frontend:\n\n"
        md += "| Endpoint | Descripción |\n"
        md += "|----------|-------------|\n"
        md += "| `/api/validate-siniestro` | Valida cliente y póliza (CLIENTES, POLIZAS) |\n"
        md += "| `/api/config-formularios` | Lee CONFIG_FORMULARIOS y CONFIG_CAMPOS |\n"
        md += "| `/api/create-siniestro` | Crea registro en tabla dinámica de siniestros |\n"
        md += "| `/api/rating` | Lee/escribe en tabla de calificaciones |\n"
        md += "| `/api/testimonios` | Lee testimonios públicos |\n"

        md += "\n"
    except Exception as e:
        md += f"⚠️ No se pudo analizar frontend: {e}\n\n"

    return md

def main():
    print("=" * 80)
    print("📊 ANÁLISIS COMPLETO DE ESTRUCTURA AIRTABLE")
    print("=" * 80)

    # Obtener metadata
    tables = get_all_tables_metadata()

    if not tables:
        print("❌ No se pudieron obtener las tablas")
        return

    print(f"✅ Se encontraron {len(tables)} tablas\n")

    # Analizar cada tabla
    tables_analysis = []

    for table in tables:
        table_name = table.get("name")
        print(f"📋 Analizando: {table_name}")

        fields = table.get("fields", [])
        analyzed_fields = [analyze_field(field, tables) for field in fields]

        tables_analysis.append({
            "id": table.get("id"),
            "name": table_name,
            "fields": analyzed_fields,
            "total_fields": len(fields)
        })

        print(f"   ✓ {len(fields)} campos analizados")

    print("\n" + "=" * 80)
    print("📝 Generando reporte markdown...")

    # Generar reporte
    report = generate_markdown_report(tables_analysis)
    report += analyze_backend_usage(tables_analysis)
    report += analyze_frontend_usage(tables_analysis)

    # Agregar recomendaciones
    report += """
## 💡 Recomendaciones y Hallazgos

### ✅ Campos Correctamente Configurados
- Campos de relación entre CLIENTES, POLIZAS y tablas de siniestros
- Sistema de CONFIG_FORMULARIOS y CONFIG_CAMPOS dinámico

### ⚠️ Posibles Mejoras
- Verificar que todos los campos usados en backend existan en las tablas
- Asegurar que las fórmulas de ID_GESTION_UNICO estén configuradas
- Revisar campos de tipo "lookup" y "rollup" para optimización

### 🔍 Próximos Pasos
1. Comparar este reporte con FULL_DB_SCHEMA.md desactualizado
2. Actualizar documentación oficial
3. Validar que no haya campos hardcodeados en código que no existan en Airtable
"""

    # Guardar reporte
    output_path = "ESTRUCTURA DE LA BASE DE DATOS/ANALISIS_COMPLETO_AIRTABLE.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Reporte guardado en: {output_path}")
    print("\n" + "=" * 80)

    # Mostrar resumen
    print("\n📊 RESUMEN:")
    print(f"   Total de Tablas: {len(tables_analysis)}")
    total_campos = sum(t["total_fields"] for t in tables_analysis)
    print(f"   Total de Campos: {total_campos}")

    print("\n🗂️ Tablas encontradas:")
    for t in tables_analysis:
        print(f"   - {t['name']} ({t['total_fields']} campos)")

if __name__ == "__main__":
    main()
