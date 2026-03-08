---
# DOCUMENTACIÓN DE DESPLIEGUE Y CONFIGURACIÓN

## Requisitos
- Python 3.8+
- Node.js 14+
- Acceso a Airtable API (API Key y Base ID, definir en .env)
- Permisos para crear y leer archivos en el sistema (se necesario para uploads)

## Instalación y Configuración

1. Clonar el repositorio:
   ```sh
git clone <repo-url>
```
2. Instalar dependencias backend:
   ```sh
pip install -r requirements.txt
```
3. Instalar dependencias frontend:
   ```sh
cd linktree  
npm install
```
4. Crear archivo `.env` en la raíz con tus credenciales:
   ```env
AIRTABLE_API_KEY=tu_apikey
AIRTABLE_BASE_ID=tu_baseid
```
5. Revisar estructura para que los campos configurados en Airtable coincidan con los del frontend y backend.

## Ejecución

- Backend (Python):
  ```sh
python main.py
```
- Frontend (Linktree):
  Servir con cualquier webserver o abrir `index.html` en navegador.

## Flujos Principales
- **Los formularios se generan de forma 100% dinámica desde la configuración almacenada en las tablas `CONFIG_FORMULARIOS` y `CONFIG_CAMPOS` de Airtable.**
- Cualquier cambio (nuevos formularios, campos, requeridos, tipos, opciones) realizado en Airtable se refleja automáticamente en el backend y frontend, sin necesidad de editar código.
- El backend expone el endpoint `/api/config-formularios` que compone y sirve la estructura de formularios según la última configuración.
- El frontend consume esta estructura y renderiza la UI, validando requeridos/tipos/opciones conforme a Airtable.
- El sistema comprime imágenes y adjuntos, envía a backend por `multipart/form-data`, y mapea automáticamente los campos según la configuración.
- Feedback visual cubre éxito, error y advertencias, alineado a la configuración dinámica.

## Estructura de directorios y archivos clave
- `/main.py`: Backend principal.
- `/linktree/app.js`: Lógica dinámica de frontend.
- `/ejecucion/`: Incluye scripts de prueba y validación.
- `/ESTRUCTURA DE LA BASE DE DATOS/`: Documentación, schemas y análisis de tablas.

## Edge Cases y Auditoría
- Ejemplo: Si un campo requerido se elimina o agrega en Airtable, el backend/frontend lo reflejan instantáneamente.
- Campos vacíos, adjuntos corruptos, límite máximo de archivos, tipos nuevos/no soportados; el feedback refleja todos estos casos según la última config.
- Para auditar el sistema: basta modificar la config en Airtable y verificar cómo el frontend/backend adaptan la UI y validaciones.

---
