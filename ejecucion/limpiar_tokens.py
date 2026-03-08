#!/usr/bin/env python3
"""
Script: limpiar_tokens.py
Objetivo: Eliminar tokens expirados o usados de Airtable

Uso: python3 limpiar_tokens.py
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN', 'patXXX_REMOVED_XXX')
BASE_ID = 'appuhslj3GFf60Tea'
TABLE_NAME = 'Tokens'
API_URL = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}'

HEADERS = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}

def obtener_todos_los_tokens():
    """Obtiene todos los registros de la tabla Tokens"""
    registros = []
    offset = None
    
    while True:
        params = {}
        if offset:
            params['offset'] = offset
            
        response = requests.get(API_URL, headers=HEADERS, params=params)
        data = response.json()
        
        registros.extend(data.get('records', []))
        offset = data.get('offset')
        
        if not offset:
            break
            
    return registros

def token_esta_expirado(registro):
    """Verifica si un token está expirado o ya fue usado"""
    fields = registro.get('fields', {})
    
    # Si ya fue usado, eliminar
    if fields.get('USADO', False):
        return True
    
    # Si expiró, eliminar
    expira_str = fields.get('EXPIRA', '')
    if expira_str:
        try:
            expira = datetime.fromisoformat(expira_str.replace('Z', '+00:00'))
            ahora = datetime.now(expira.tzinfo) if expira.tzinfo else datetime.now()
            if ahora > expira:
                return True
        except:
            pass
    
    return False

def eliminar_registro(record_id):
    """Elimina un registro de Airtable"""
    url = f'{API_URL}/{record_id}'
    response = requests.delete(url, headers=HEADERS)
    return response.status_code == 200

def main():
    print("🔍 Obteniendo tokens de Airtable...")
    tokens = obtener_todos_los_tokens()
    print(f"   Total de tokens: {len(tokens)}")
    
    # Filtrar tokens a eliminar
    tokens_a_eliminar = [t for t in tokens if token_esta_expirado(t)]
    print(f"   Tokens expirados/usados: {len(tokens_a_eliminar)}")
    
    if not tokens_a_eliminar:
        print("✅ No hay tokens para limpiar")
        return
    
    # Eliminar tokens
    print("🗑️ Eliminando tokens...")
    eliminados = 0
    errores = 0
    
    for token in tokens_a_eliminar:
        if eliminar_registro(token['id']):
            eliminados += 1
        else:
            errores += 1
    
    print(f"\n📊 Resumen:")
    print(f"   ✅ Eliminados: {eliminados}")
    print(f"   ❌ Errores: {errores}")
    print(f"   📁 Tokens restantes: {len(tokens) - eliminados}")

if __name__ == '__main__':
    main()
