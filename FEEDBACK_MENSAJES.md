---
# FEEDBACK VISUAL Y MENSAJES (FRONTEND Y BACKEND)

## FRONTEND
- Todos los mensajes son claros y visuales usando Swal.fire.
- Estados cubiertos:
    - Éxito: Denuncia enviada, archivos subidos.
    - Advertencia: Algunos archivos fallidos, campos faltantes, límite de archivos.
    - Error: Tiempo agotado, JSON inválido, conexión.
- Mensajes incluyen detalles, número de gestión y explican cada edge case.

## BACKEND
- Respuestas detalladas:
    - `status`: success/warning/error
    - `message`: explicación del estado
    - `archivos_subidos`: cantidad exitosa
    - `archivos_fallidos`: nombres de fallidos
    - Si campo inválido: mensaje de que falta en la configuración.
- Log de errores para debugging: imprime exceptions con contexto.

---
