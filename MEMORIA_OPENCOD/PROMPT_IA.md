# 📝 PROMPT PARA IA - Problema Railway

---

## CONTEXTO

Tengo un sistema de seguros agenticos con:
- **Backend Python (FastAPI)** desplegado en Railway
- **Frontend (Linktree)** en Surge.sh
- **Base de datos** en Airtable
- **n8n** también en Railway (misma app)

## EL PROBLEMA

Railway tiene cacheada una versión vieja del código Python y no actualiza aunque hago push a GitHub.

### Síntomas:
- Los logs del backend muestran "v4" aunque el código local ya está en "v9"
- Llevo 5+ redeploys manuales y no actualiza
- Los cambios no se reflejan

### Código actual en GitHub:
- Commits hasta "v9" subidos correctamente
- El código tiene la lógica para subir imágenes a ImgBB

## DATOS TÉCNICOS

- **Repo:** https://github.com/grupoprosperyn8n/backend-seguros
- **App Railway:** web-production-2584d.up.railway.app
- **Variables necesarias en Railway:**
  - AIRTABLE_API_KEY
  - AIRTABLE_BASE_ID (appuhslj3GFf60Tea)

## LO QUE NECESITO

1. ¿Cómo puedo hacer que Railway tome los cambios de GitHub?
2. ¿O es mejor crear una nueva app de Railway solo para el backend Python?
3. ¿Qué consecuencias tiene crear una nueva app (nueva URL, etc)?

## NOTA EXTRA

El problema de fondo es que las imágenes no se suben a ImgBB - el código está listo pero Railway tiene la versión vieja que usa Airtable Content API (que no funciona).

