---
# EJEMPLOS DE INTEGRACIÓN Y EDGE CASES

## Ejemplo de payload frontend (con adjuntos)
- Campos enviados:
  - nombre
  - fecha
  - descripción
  - adjuntos[]
- Ejemplo:
```
nombre: Juan Perez
fecha: 2026-03-05
descripción: Choque en Av. Corrientes
adjuntos: [foto1.jpg, foto2.jpg]
```

## Ejemplo de respuesta backend
```
{
  "status": "success",
  "message": "Siniestro reportado correctamente",
  "archivos_subidos": 2
}
```

## Edge Cases
- **Archivos corruptos**: El feedback muestra error y el siniestro no se crea.
- **Campos faltantes**: El sistema devuelve advertencia y pide completar campos.
- **Límite de archivos (max 5)**: Si se adjuntan más, solo los primeros 5 se procesan y se muestra advertencia.
- **Campo vacío**: El sistema lo identifica y muestra mensaje.

## Ejemplo de cambio de configuración (dinámica real)
- Agregar un campo nuevo en `CONFIG_CAMPOS` en Airtable:
   - El campo aparece automáticamente al recargar el frontend (sin modificar el código).
- Eliminar un campo requerido, cambiar tipo/opciones:
   - El cambio se refleja en la UI y en validaciones/feedback.
- Modificar el nombre, help text, required o restricciones desde Airtable:
   - Todas las validaciones y textos cambian en tiempo real.

## Ejemplo de test manual
- Reportar siniestro solo con datos (sin adjuntos).
- Reportar siniestro con imágenes grandes y verificar compresión.
- Reportar siniestro con campo faltante y comprobar el feedback.
- Actualizar config en Airtable y auditar cómo se adapta el sistema: UI, validaciones, envíos, feedback.

---
