#!/bin/bash

echo "================================================================================"
echo "🔍 VERIFICACIÓN PRE-PUSH - Backend Seguros"
echo "================================================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ ERROR: Ejecuta este script desde el directorio backend/"
    exit 1
fi

# Mostrar rama actual
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Rama actual: $BRANCH"

# Mostrar commits pendientes
PENDING=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")
echo "📦 Commits pendientes de push: $PENDING"
echo ""

if [ "$PENDING" = "0" ]; then
    echo "✅ No hay commits pendientes. Todo está sincronizado."
    exit 0
fi

# Mostrar los commits que se van a subir
echo "📝 COMMITS QUE SE VAN A SUBIR:"
echo "----------------------------------------------------------------------------"
git log origin/main..HEAD --oneline --color=always
echo ""

# Mostrar archivos modificados en los commits
echo "📄 ARCHIVOS MODIFICADOS:"
echo "----------------------------------------------------------------------------"
git diff --stat origin/main..HEAD
echo ""

# Verificar runtime.txt
echo "🔍 VERIFICANDO runtime.txt:"
echo "----------------------------------------------------------------------------"
if grep -q "python-3.12" runtime.txt; then
    echo "✅ runtime.txt contiene: $(cat runtime.txt | tr -d '\n')"
    echo "   (Correcto para Railway)"
elif grep -q "python-3.11" runtime.txt; then
    echo "⚠️  runtime.txt contiene: $(cat runtime.txt | tr -d '\n')"
    echo "   NOTA: Debería ser python-3.12 pero ya está en commits locales"
else
    echo "❓ runtime.txt contiene: $(cat runtime.txt | tr -d '\n')"
fi
echo ""

# Verificar conectividad con GitHub
echo "🌐 VERIFICANDO CONEXIÓN CON GITHUB:"
echo "----------------------------------------------------------------------------"
REMOTE_URL=$(git remote get-url origin)
echo "   Remote URL: $REMOTE_URL"

if git ls-remote origin HEAD > /dev/null 2>&1; then
    echo "✅ Conexión exitosa con GitHub"
else
    echo "⚠️  No se puede conectar con GitHub"
    echo "   Verifica tu conexión a internet o credenciales"
fi
echo ""

# Instrucciones finales
echo "================================================================================"
echo "🚀 LISTO PARA HACER PUSH"
echo "================================================================================"
echo ""
echo "Para subir los cambios a GitHub y desplegar en Railway, ejecuta:"
echo ""
echo "   git push origin main"
echo ""
echo "Se te pedirá:"
echo "   Username: grupoprosperyn8n"
echo "   Password: [Tu Personal Access Token de GitHub]"
echo ""
echo "💡 Si no tienes Token:"
echo "   1. Ir a: https://github.com/settings/tokens"
echo "   2. Generate new token (classic)"
echo "   3. Permisos: ✅ repo"
echo "   4. Copiar token y usarlo como password"
echo ""
echo "📖 Guía completa en: HACER_PUSH.md"
echo ""
echo "================================================================================"
