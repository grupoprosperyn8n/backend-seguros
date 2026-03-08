#!/usr/bin/env python3
"""
Script para actualizar ETIQUETA_POLIZA en Airtable con formato completo.
"""
from pyairtable import Table
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Conectar a tabla POLIZAS
table_polizas = Table(API_KEY, BASE_ID, 'POLIZAS')

# Buscar la póliza con patente PDL384
formula = 'SEARCH("PDL384", {PATENTE DEL VEHICULO})'
records = table_polizas.all(formula=formula, max_records=5)

print(f"Encontradas {len(records)} pólizas con PDL384:")
for r in records:
    fields = r['fields']
    print(f"\nID: {r['id']}")
    print(f"  Número: {fields.get('POLIZA N°', 'N/A')}")
    print(f"  Patente: {fields.get('PATENTE DEL VEHICULO', 'N/A')}")
    print(f"  Tipo: {fields.get('TIPO DE VEHICULO', 'N/A')}")
    print(f"  Categoría: {fields.get('CATEGORIA', 'N/A')}")
    print(f"  Vida: {fields.get('VIDA', 'N/A')}")
    print(f"  Auxilio: {fields.get('AUXILIO MECANICO', 'N/A')}")
    print(f"  Estado: {fields.get('ESTADO', 'N/A')}")
    print(f"  Vencimiento: {fields.get('FECHA VENCIMIENTO DE LA POLIZA', 'N/A')}")
    
    # Mostrar ETIQUETA_POLIZA actual
    etiqueta = fields.get('ETIQUETA_POLIZA', 'N/A')
    print(f"  ETIQUETA_POLIZA actual: {etiqueta}")
