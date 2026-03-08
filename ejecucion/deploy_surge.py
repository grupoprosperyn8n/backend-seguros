#!/usr/bin/env python3
"""
Script: deploy_surge.py
Objetivo: Desplegar frontend a Surge.sh

Uso: python3 deploy_surge.py [--registro] [--linktree]
     --registro: despliega el sitio de registro también
     --linktree: despliega el sitio linktree al dominio de login (sobrescribe login)
"""

import subprocess
import sys
import os

# Configuración
PROYECTO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(PROYECTO_PATH, 'SaaS-Login')
LINKTREE_PATH = os.path.join(PROYECTO_PATH, 'linktree')

DOMINIOS = {
    'login': 'login-agentico-1770227340.surge.sh',
    'registro': 'registro-agentico-1770227370.surge.sh',
    'linktree': 'seguros-app-linktree.surge.sh'
}

def deploy_to_surge(source_path, domain):
    """Ejecuta el deploy a Surge.sh"""
    print(f"🚀 Desplegando {os.path.basename(source_path)} a {domain}...")
    
    cmd = ['npx', 'surge', source_path, '--domain', domain]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=source_path)
        
        if result.returncode == 0:
            print(f"✅ Deploy exitoso: https://{domain}")
            return True
        else:
            print(f"❌ Error en deploy:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    incluir_registro = '--registro' in sys.argv
    is_linktree = '--linktree' in sys.argv
    
    print("=" * 50)
    print("📦 Deploy Frontend - Sistema de Seguros")
    print("=" * 50)
    
    login_ok = True
    
    if is_linktree:
        # Deploy Linktree al dominio de linktree
        login_ok = deploy_to_surge(LINKTREE_PATH, DOMINIOS['linktree'])
    else:
        # Deploy Login (SaaS-Login)
        login_ok = deploy_to_surge(FRONTEND_PATH, DOMINIOS['login'])
    
    # Deploy registro (opcional)
    registro_ok = True
    if incluir_registro:
        registro_ok = deploy_to_surge(FRONTEND_PATH, DOMINIOS['registro'])
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   {'Linktree' if is_linktree else 'Login'}: {'✅' if login_ok else '❌'}")
    if incluir_registro:
        print(f"   Registro: {'✅' if registro_ok else '❌'}")
    print("=" * 50)
    
    return 0 if (login_ok and registro_ok) else 1

if __name__ == '__main__':
    sys.exit(main())
