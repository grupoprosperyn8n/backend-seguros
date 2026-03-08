"""
Script para crear las nuevas tablas en Airtable:
1. FAQ - Preguntas Frecuentes
2. QUIENES_SOMOS - Información de la empresa
"""

import os
from pyairtable import Api

# Cargar variables de entorno
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

api = Api(API_KEY)

# ==============================================================================
# TABLA 1: FAQ - PREGUNTAS FRECUENTES
# ==============================================================================

faq_schema = {
    "name": "FAQ",
    "description": "Tabla para gestionar Preguntas Frecuentes del sitio",
    "fields": [
        {
            "name": "PREGUNTA",
            "type": "richText",
            "description": "La pregunta frecuente",
        },
        {
            "name": "RESPUESTA",
            "type": "richText",
            "description": "La respuesta a la pregunta",
        },
        {
            "name": "CATEGORIA",
            "type": "multilineText",
            "description": "Categoría de la pregunta (ej: Siniestros, Cotización, General)",
        },
        {
            "name": "ORDEN",
            "type": "number",
            "options": {"precision": 0},
            "description": "Orden de aparición",
        },
        {
            "name": "VISIBLE",
            "type": "checkbox",
            "description": "Mostrar en el sitio web",
        },
        {
            "name": "ICONO",
            "type": "singleLineText",
            "description": "Icono FontAwesome (ej: fa-question-circle)",
        },
    ],
}

# ==============================================================================
# TABLA 2: QUIENES SOMOS
# ==============================================================================

quienes_somos_schema = {
    "name": "QUIENES_SOMOS",
    "description": "Tabla para gestionar la información de Quiénes Somos",
    "fields": [
        {
            "name": "TITULO",
            "type": "richText",
            "description": "Título principal (ej: Rafael Allende & Asociados)",
        },
        {
            "name": "SUBTITULO",
            "type": "richText",
            "description": " Subtítulo o eslogan",
        },
        {
            "name": "TEXTO PRINCIPAL",
            "type": "richText",
            "description": "Descripción principal de la empresa",
        },
        {
            "name": "NOMBRE RESPONSABLE",
            "type": "singleLineText",
            "description": "Nombre del responsable/gerente",
        },
        {
            "name": "CARGO",
            "type": "singleLineText",
            "description": "Cargo del responsable",
        },
        {
            "name": "FOTO PERFIL",
            "type": "multipleAttachments",
            "description": "Foto de perfil del responsable",
        },
        {
            "name": "AÑOS EXPERIENCIA",
            "type": "number",
            "options": {"precision": 0},
            "description": "Años de experiencia en el mercado",
        },
        {
            "name": "CANTIDAD CLIENTES",
            "type": "number",
            "options": {"precision": 0},
            "description": "Cantidad de clientes atendidos",
        },
        {
            "name": "CANTIDAD SUCURSALES",
            "type": "number",
            "options": {"precision": 0},
            "description": "Cantidad de sucursales",
        },
        {
            "name": "CANTIDAD POLIZAS",
            "type": "number",
            "options": {"precision": 0},
            "description": "Pólizas gestionadas",
        },
        {
            "name": "MISIÓN",
            "type": "multilineText",
            "description": "Misión de la empresa",
        },
        {
            "name": "VISIÓN",
            "type": "multilineText",
            "description": "Visión de la empresa",
        },
        {
            "name": "VALORES",
            "type": "multilineText",
            "description": "Valores de la empresa (separados por coma)",
        },
        {
            "name": "IMAGEN FONDO",
            "type": "multipleAttachments",
            "description": "Imagen de fondo para la sección",
        },
        {
            "name": "COLOR PRINCIPAL",
            "type": "singleLineText",
            "description": "Color principal en hex (ej: #1e40af)",
        },
        {
            "name": "COLOR SECUNDARIO",
            "type": "singleLineText",
            "description": "Color secundario en hex",
        },
        {
            "name": "VIDEO PRESENTACIÓN",
            "type": "url",
            "description": "URL del video de presentación",
        },
        {
            "name": "MOSTRAR ESTADÍSTICAS",
            "type": "checkbox",
            "description": "Mostrar las estadísticas (clientes, sucursales, etc)",
        },
        {
            "name": "VISIBLE",
            "type": "checkbox",
            "description": "Mostrar la sección en el sitio",
        },
    ],
}


def create_table(schema):
    """Crea una tabla en Airtable"""
    try:
        table = api.create_table(BASE_ID, schema)
        print(f"✅ Tabla creada: {table['name']} (ID: {table['id']})")
        return table
    except Exception as e:
        print(f"❌ Error creando tabla {schema['name']}: {e}")
        return None


if __name__ == "__main__":
    print("🚀 Creando tablas en Airtable...")

    # Crear tabla FAQ
    print("\n📝 Creando tabla FAQ...")
    faq_table = create_table(faq_schema)

    # Crear tabla QUIENES_SOMOS
    print("\n📝 Creando tabla QUIENES_SOMOS...")
    qs_table = create_table(quienes_somos_schema)

    print("\n✅ Proceso completado!")
    print("\n📋 Resumen de IDs de tablas:")
    if faq_table:
        print(f"  FAQ: {faq_table['id']}")
    if qs_table:
        print(f"  QUIENES_SOMOS: {qs_table['id']}")
