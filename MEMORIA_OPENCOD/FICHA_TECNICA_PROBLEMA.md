# 📋 FICHA TÉCNICA - Problema Railway + Carga de Imágenes

---

## 🎯 ESTADO ACTUAL DEL SISTEMA

| Componente | Estado | URL |
|------------|--------|-----|
| Backend Python (FastAPI) | ❌ Railway cacheado con versión vieja | web-production-2584d.up.railway.app |
| Frontend (Linktree) | ✅ Actualizado | seguros-app-linktree.surge.sh |
| Airtable | ✅ Funcionando | appuhslj3GFf60Tea |
| n8n | ✅ Funcionando | Mismo Railway |

---

## 🔴 PROBLEMA PRINCIPAL

**Railway no actualiza el código** - tiene cacheada una versión vieja del backend y no detecta los nuevos commits de GitHub.

### Síntomas:
- Los logs muestran "v4" aunque el código local ya está en "v9"
- Los cambios no se reflejan después deredeploy
- El redeploy manual no funciona

---

## 📝 PROBLEMA SECUNDARIO (la causa real)

**Las imágenes no se suben a ImgBB** - El código tiene la lógica correcta, pero Railway tiene la versión vieja que usa Airtable Content API (que no funciona).

### Causa raíz:
- El frontend envía las fotos como objetos UploadFile
- Railway (versión vieja) recibe strings "UploadFile" en vez de objetos reales
- Por eso no detecta los archivos y no los sube

---

## 🔧 LO QUE SE HA INTENTADO

1. ✅ Cambios en el código local (v5 → v9)
2. ✅ Push a GitHub - exitoso
3. ✅ Redeploy manual en Railway - NO funciona
4. ✅ Múltiples redeploys - mismos resultados
5. ✅ Actualizar Surge (linktree) - exitoso

---

## 💡 SOLUCIONES POSIBLES

### Opción A: Nueva app de Railway (RECOMENDADA)
- Crear app nueva solo para backend Python
- Vinculada a GitHub
- Ventaja: App limpia, actualizaciones automáticas
- Desventaja: Nueva URL, hay que actualizar el frontend

### Opción B: Forzar cache refresh
- Borrar cache de Railway
- Cambiar nombre del archivo main.py
- Esperar que funcione

### Opción C: Cambiar de proveedor
- Migrar a Render, Heroku, o similar

---

## 📌 PUNTO ACTUAL (RESUELTO)

- **Estado:** 🟢 RESUELTO.
- **Causa Raíz Encontrada:** El payload de Airtable exigía explícitamente formato `[{"url": "https://..."}]` para insertar adjuntos y nosotros mandábamos un string plano, lo cual abortaba la escritura de forma silenciosa. Además, Railway no re-desplegaba por tener atascados los workers viejos (se solucionó forzando updates atómicos via GitHub API y manual redeploy).
- **Punto Actual:** Siniestros carga fotos en ImgBB, impacta en Airtable de forma instantánea y devuelve comprobante físico/compartible al cliente con su número de código de gestión `ID_UNICO_GESTION`.
- **Código local:** 100% operativo.
- **GitHub:** Actualizado.
- **Railway:** Deploy v9 corriendo.
- **Linktree (Surge):** Actualizado y funcionando con botón de 'Descargar Comprobante'.

---

## 🎯 LO QUE SE NECESITA

- 🟢 **NADA.** El sistema ha quedado completamente operativo.
