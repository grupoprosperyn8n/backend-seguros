---
# INSTRUCCIONES DE USO (FRONTEND Y BACKEND)

## FRONTEND
1. Abre el `index.html` del directorio linktree en el navegador.
2. El formulario que ves se genera completamente desde la configuración dinámica de Airtable (`CONFIG_FORMULARIOS` y `CONFIG_CAMPOS`).
   - Si se agrega un nuevo formulario o campo en Airtable, aparecerá automáticamente en el frontend.
   - Si se edita/elimina un campo o se cambia un required/type, el cambio se refleja en tiempo real (tras recargar).
3. Completa los campos según los requeridos/opciones/configuración proveniente de Airtable. Adjunta imágenes/documentos si el campo lo permite.
4. Al enviar, el feedback visual cubrirá éxito, advertencias, errores y validaciones conforme a la última config de Airtable.
5. El sistema valida campos obligatorios/tipo/opciones completamente de manera dinámica; nunca hay formularios fijos.

## BACKEND
1. Ejecuta `main.py` para levantar el backend.
2. El endpoint `/api/create_siniestro` espera datos y archivos en formato `multipart/form-data`.
3. El backend mapea automáticamente los campos y adjuntos a Airtable.
4. La respuesta siempre incluye estado, mensaje y detalles del upload.

---
## INSTRUCCIONES PARA PRUEBAS

- Usa los scripts del directorio `ejecucion` para pruebas de carga y envío.
- Para validar edge cases, modifica los campos en el frontend y verifica el feedback.
- Los tests se ejecutan con `pytest` si el entorno lo permite.

---
