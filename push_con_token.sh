#!/bin/bash

echo "================================================================================"
echo "🚀 PUSH AUTOMÁTICO CON TOKEN"
echo "================================================================================"
echo ""

# Verificar directorio
if [ ! -f "main.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio backend/"
    exit 1
fi

# Pedir token
echo "Por favor, pega tu GitHub Personal Access Token:"
echo "(El token NO se mostrará en pantalla por seguridad)"
echo ""
read -s -p "Token: " GITHUB_TOKEN
echo ""
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: Token vacío"
    exit 1
fi

echo "🔧 Configurando remote con token..."
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/grupoprosperyn8n/backend-seguros.git"

echo "📤 Haciendo push a origin main..."
git push origin main

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo "✅ PUSH EXITOSO"
    echo "================================================================================"
    echo ""
    echo "Los cambios fueron subidos correctamente."
    echo "Railway detectará los cambios en ~30 segundos."
    echo ""
    echo "Verificar en:"
    echo "  GitHub: https://github.com/grupoprosperyn8n/backend-seguros/commits/main"
    echo "  Railway: Ver logs de deployment"
    echo ""
else
    echo ""
    echo "❌ ERROR EN EL PUSH"
    echo ""
    echo "Posibles causas:"
    echo "  - Token inválido o expirado"
    echo "  - Token sin permisos 'repo'"
    echo "  - Problema de conexión"
    echo ""
    echo "Genera un nuevo token en:"
    echo "  https://github.com/settings/tokens/new"
    echo ""
    exit 1
fi

# Limpiar token del remote por seguridad
echo "🧹 Limpiando token del remote..."
git remote set-url origin "https://grupoprosperyn8n:@github.com/grupoprosperyn8n/backend-seguros.git"

echo "🔒 Token removido del historial de git (seguridad)"
echo ""
echo "================================================================================"
