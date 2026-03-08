---
# VALIDACIÓN MANUAL Y EDGE CASES

Se han reportado manualmente los siguientes casos:

1. **Siniestro sin adjuntos**:
   - Estado: éxito
   - Mensaje recibido: "Siniestro reportado correctamente"

2. **Siniestro con campos vacíos**:
   - Estado: advertencia
   - Mensaje recibido: "Completa todos los campos requeridos"

3. **Siniestro con adjuntos grandes/corruptos**:
   - Estado: error
   - Mensaje recibido: "El archivo adjunto no es válido"

4. **Siniestro con más de 5 adjuntos**:
   - Estado: advertencia
   - Mensaje recibido: "Solo se procesarán los primeros 5 archivos"

5. **Siniestro normal (con datos completos y hasta 5 adjuntos)**:
   - Estado: éxito
   - Mensaje recibido: "Siniestro reportado correctamente"

Todos estos casos están cubiertos por el feedback del sistema y la lógica de flujo.

---
