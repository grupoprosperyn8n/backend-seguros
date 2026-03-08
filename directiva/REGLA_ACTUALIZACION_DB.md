# ⚖️ REGLA: Mantenimiento de Estructura de Datos

## ⚠️ PRINCIPIO DE VERDAD
El archivo `ESTRUCTURA DE LA BASE DE DATOS/FULL_DB_SCHEMA.md` es la **ÚNICA FUENTE DE VERDAD** sobre la estructura de Airtable.

## 📝 Procedimiento Obligatorio
Cada vez que se realice un cambio en Airtable (Agregar columna, cambiar fórmula, crear tabla):

1.  **ACTUALIZAR INMEDIATAMENTE** el archivo `FULL_DB_SCHEMA.md` con los nuevos detalles.
2.  Mantener el formato de tabla existente.
3.  Registrar la fecha de última modificación en el encabezado del archivo.

## 🚫 Prohibiciones
*   NO crear automatizaciones basadas en campos que no estén documentados aquí.
*   NO modificar nombres de campos en Airtable sin actualizar este documento PRIMERO.

## 🤖 Para Agentes de IA
Si vas a leer o escribir en Airtable:
1.  **LEE** este archivo primero para conocer los nombres exactos de columnas.
2.  Si encuentras discrepancias, **AVISA** al usuario y sugiere una actualización del documento.
