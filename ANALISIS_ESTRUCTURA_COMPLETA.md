# 🔍 ANÁLISIS EXHAUSTIVO: Estructura Airtable vs Frontend vs Backend

**Fecha:** 2026-03-03
**Base Airtable:** `appuhslj3GFf60Tea`
**Total Tablas:** 21
**Total Campos:** 710

---

## 📊 RESUMEN EJECUTIVO

### Estado General
- ✅ **Sistema dinámico funcionando:** CONFIG_FORMULARIOS + CONFIG_CAMPOS permiten crear formularios sin código
- ⚠️ **Documentación desactualizada:** FULL_DB_SCHEMA.md es de feb 2024 (hace 13 meses)
- 🔴 **Campos críticos faltantes identificados**
- 🟡 **Nomenclatura inconsistente** entre tablas

### Hallazgos Críticos
1. Las 3 tablas de siniestros tienen estructuras muy diferentes (152, 86, 86 campos)
2. Campo `ESTADO_WEB` solo existe en código Python, no documentado en Airtable
3. Múltiples campos "de respaldo" (DENUNCIA OC 2, 3, 4, 5) indican refactorizaciones previas
4. Sistema de CONFIG funcional pero sin validación de que campos existan en tablas destino

---

## 🗂️ TABLAS PRINCIPALES Y SU PROPÓSITO

### 1. **CLIENTES** (43 campos)
**Propósito:** Tabla maestra de clientes

**Campos Clave:**
- `DNI` (Número) - Usado para validación en frontend
- `NOMBRES` + `APELLIDO` (Texto)
- `TELEFONO` (Teléfono), `EMAIL` (Email)
- `ETIQUETA_POLIZA Compilación` (Rollup) - **CRÍTICO para validación de siniestros**

**Relaciones:**
- → POLIZAS (vinculación directa)
- → DENUNCIA DE ACCIDENTE
- → DENUNCIA ROBO OC
- → DENUNCIA ROBO / INCENDIO
- → CALIFICACIONES
- → EMPLEADOS (asesor asignado)

**Uso en Backend:**
- `backend/main.py:571-643` - Validación de siniestros
- Búsqueda por DNI con fórmula: `({DNI} & "") = "12345678"`

**Conexión Frontend:**
- `linktree/app.js:840-896` - Función `validarClienteSiniestro()`
- Endpoint: `/api/validate-siniestro?dni=XXX&patente=YYY`

**Problemas Identificados:**
- ⚠️ Campo `ETIQUETA_POLIZA Compilación` usa parsing de texto con emojis (frágil)
- ✅ Tiene campo `NOMBRE COMPLETO` como fórmula concatenada
- 🟡 9 campos de rollup/count para métricas (puede ralentizar queries)

---

### 2. **POLIZAS** (40 campos)
**Propósito:** Registro de pólizas de seguros

**Campos Clave:**
- `N° DE POLIZA` (Texto) - Identificador único
- `PATENTE DEL VEHICULO` (Texto) - Usado en validación
- `ESTADO DE LA POLIZA` (Select): ALTA, ANULACION, EN TRAMITE, VIGENTE
- `MARCA DEL VEHICULO`, `MODELO DEL VEHICULO`, `AÑO DEL VEHICULO`
- `COBERTURA` (Select): A, B, B1, B2, B3, B4, B5, C, D, E, F, G
- `VIDA` (Select): Si, No, N CREDITO
- `AUXILIO` (Select): AUX, AUX 300, AUX 500, AUX 1000, AUX INFINITY
- `ETIQUETA_POLIZA` (Fórmula) - **Genera el texto que se usa en validación**

**Relaciones:**
- → CLIENTES 2 (cliente titular)
- → COMPANIA LINK (aseguradora)
- → PRODUCTO LINK (tipo de seguro)
- → Todas las tablas de DENUNCIA

**Uso en Backend:**
- `backend/main.py:606-678` - Parsing del campo ETIQUETA_POLIZA
- Se busca la patente dentro de la compilación de texto

**Fórmula ETIQUETA_POLIZA (parcial):**
```
SWITCH({ESTADO},
  "VIGENTE", "✅ VENCE " & fecha & " | " & patente & " | " & marca,
  "ANULACION", "❌ ANULADA " & fecha & " | " & patente,
  ...
)
```

**Problemas Identificados:**
- 🔴 **CRÍTICO:** El sistema depende 100% del formato de esta fórmula
- ⚠️ Si se cambia emoji ✅ a otro, validación falla
- ⚠️ Múltiples relaciones duplicadas (DENUNCIA ROBO OC 3, 4, 5) - legacy code
- 🟡 No tiene campo `PATENTE_NORMALIZADA` (limpia de espacios/guiones)

---

### 3. **DENUNCIA DE ACCIDENTE** (152 campos!!!)
**Propósito:** Registra choques, granizo, daños totales/parciales

**Campos Clave:**
- `ID_GESTION_UNICO` (Fórmula) - ID único autogenerado
- `FECHA DEL SINIESTRO` (Fecha)
- `HORA APROX. DEL SINIESTRO` (Número)
- `DIRECCIÓN Y N°`, `INTERSECCIÓN O ENTRE CALLES`, `LUGAR O ESTABLECIMIENTO`
- `RELATOS DEL HECHO` (Texto largo) - **Campo flexible para datos extras**
- `USO DEL VEHICULO` (Select): PARTICULAR, COMERCIAL, REMIS-TAXI, DELIVERY, etc.
- `CLASIFICACIÓN` (Select tipo de accidente)
- `CULPABILIDAD` (Select)
- `CULPABILIDAD IA` (Objeto JSON) - **Análisis automático con IA**
- `GOOGLE MAPS URL` (URL)
- `ESTADO_WEB` - **NO ENCONTRADO EN SCHEMA** (solo en código)

**Campos de Archivos Adjuntos:**
- `FOTOS_DNI`, `FOTO_CARNET`, `FOTOS_DANOS`, `DENUNCIA_POLICIAL`
- Cada uno puede tener múltiples archivos

**Relaciones:**
- → CLIENTE
- → POLIZAS
- → EMPLEADOS (quien cargó)
- → OFICINAS (sucursal)

**Uso en Backend:**
- `backend/main.py:841-1033` - Endpoint `/api/create-siniestro`
- Crea registro dinámicamente basándose en CONFIG_CAMPOS

**Problemas Identificados:**
- 🔴 **152 CAMPOS es excesivo** - Tabla sobrecargada
- ⚠️ Campo `ESTADO_WEB` hardcodeado en línea 981 pero no existe en schema
- 🟡 Muchos lookups/rollups hacia otras tablas (performance)
- ✅ Tiene soporte para IA en campo `CULPABILIDAD IA`

---

### 4. **DENUNCIA ROBO OC** (86 campos)
**Propósito:** Robos parciales (cristales, ruedas, baterías, espejos)

**Campos Clave:**
- `ID_UNICO_GESTION` (Fórmula)
- `CLASIFICACIÓN DEL DAÑO` - Qué se robó
- `ALCANCE DE COBERTURA`, `MOTIVOS DE LA CONSULTA`
- `VERIFICACION DE ORDEN`, `ORDEN PEDIDA A CIA`
- **NO TIENE campo específico para MEDIDAS DE RUEDAS** (se guarda en RELATOS)

**Relaciones:**
- Similar a DENUNCIA DE ACCIDENTE

**Problemas Identificados:**
- ⚠️ Nombre confuso "OC" (Otros Componentes?)
- 🟡 86 campos sigue siendo demasiado
- 🔴 Falta campo estructurado para datos de ruedas/baterías

---

### 5. **DENUNCIA ROBO / INCENDIO** (86 campos)
**Propósito:** Robo total e incendios (totales o parciales)

**Campos Clave:**
- Similar a las otras tablas de denuncia
- `TIPO_SINIESTRO` diferencia entre ROBO TOTAL e INCENDIO

**Problemas Identificados:**
- ⚠️ Mezcla 2 tipos de siniestros muy diferentes en una tabla
- 🟡 Debería separarse en 2 tablas distintas

---

### 6. **CONFIG_FORMULARIOS** (7 campos) ⭐
**Propósito:** Define qué formularios existen en el sistema

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `CODIGO` | Texto | Slug usado en frontend (ej: "choque", "robo-total") |
| `TITULO` | Texto | Título mostrado (ej: "Denuncia de Choque") |
| `ICONO` | Texto | FontAwesome class o emoji |
| `COLOR` | Texto | Color hex del botón |
| `TABLA RELACIONADA` | Texto | Nombre de tabla Airtable destino |
| `VISIBILIDAD` | Checkbox | Si está activo en el menú |
| `CONFIG_CAMPOS` | Relación | → CONFIG_CAMPOS |

**Uso en Backend:**
- `backend/main.py:721-796` - Endpoint `/api/config-formularios`
- Lee TODOS los formularios visibles y sus campos

**Uso en Frontend:**
- `linktree/app.js:775-806` - Función `loadFormConfig()`
- `linktree/app.js:809-838` - Función `renderDynamicMenu()`

**Ejemplo de Registro:**
```
CODIGO: choque
TITULO: Denuncia de Choque
ICONO: fa-car-crash
COLOR: #ef4444
TABLA RELACIONADA: DENUNCIA DE ACCIDENTE
VISIBILIDAD: ✅
```

**Validación:**
✅ Sistema funcional
⚠️ NO valida que TABLA RELACIONADA exista
⚠️ NO valida que COLUMNA AIRTABLE de campos existan

---

### 7. **CONFIG_CAMPOS** (8 campos) ⭐
**Propósito:** Define campos de cada formulario y mapeo a Airtable

**Campos:**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `ID CAMPO` | Texto | ID usado en HTML (ej: "fecha_siniestro") |
| `ETIQUETA` | Texto | Label visible (ej: "Fecha del siniestro") |
| `TIPO` | Select | text, date, file, select, textarea, etc. |
| `OPCIONES` | Texto largo | Para selects, separado por comas |
| `OBLIGATORIO` | Checkbox | Si es required |
| `ORDEN` | Número | Orden de aparición en el form |
| `FORMULARIO` | Relación | → CONFIG_FORMULARIOS (puede ser múltiple) |
| `COLUMNA AIRTABLE` | Texto | Nombre EXACTO del campo en tabla destino |

**MAPEO CRÍTICO:**
Este es el puente entre frontend y Airtable:
```
Frontend:         Backend:                    Airtable:
fecha_siniestro → field_map['fecha_siniestro'] → FECHA DEL SINIESTRO
```

**Ejemplo de Registro:**
```
ID CAMPO: fecha_siniestro
ETIQUETA: ¿Cuándo ocurrió?
TIPO: date
OBLIGATORIO: ✅
ORDEN: 1
FORMULARIO: [choque, robo-total]
COLUMNA AIRTABLE: FECHA DEL SINIESTRO
```

**Uso en Backend:**
- `backend/main.py:926-950` - Construye `field_map` para mapear IDs a columnas
```python
field_map = {}
for c_rec in campos_records:
    id_campo = c.get("ID CAMPO")
    columna = c.get("COLUMNA AIRTABLE")
    if id_campo and columna:
        field_map[id_campo] = columna
```

**Uso en Frontend:**
- `linktree/app.js:1001-1046` - Función `renderCampo(campo)`
- Genera HTML dinámico basado en campo.type

**Problemas Identificados:**
- 🔴 **NO HAY VALIDACIÓN** de que COLUMNA AIRTABLE exista en tabla destino
- 🔴 Si hay typo en COLUMNA AIRTABLE, el backend falla con "Unknown field name"
- ⚠️ No hay campo PLACEHOLDER (se usa placeholder genérico)
- ⚠️ Campo TIPO usa Select con opciones en español ("Texto de una línea") en lugar de valores técnicos ("text")

**Tipos Válidos (según código frontend):**
- `text`, `date`, `time`, `number`, `select`, `textarea`, `file`

**Tipos en Airtable (español):**
- "Single line text (Texto de una línea)"
- "Long text (Texto largo)"
- "Date (Fecha)"
- "Attachment (Archivo adjunto)"

⚠️ **HAY UN DESACOPLE:** Backend espera "text" pero Airtable tiene "Single line text"

---

### 8. **CALIFICACIONES** (17 campos)
**Propósito:** Ratings y testimonios de clientes

**Campos Clave:**
- `ESTRELLAS` (Número 1-5)
- `NOMBRE`, `DNI` (si es cliente)
- `COMENTARIO` (Texto largo)
- `ES_CLIENTE` (Checkbox)
- `SERVICIO` (Select): Atención General, Cotización, Siniestro, etc.
- `AUTORIZA_PUBLICAR` (Checkbox)
- `USAR_FOTO` (Checkbox)
- `MODO` (Select): Online, Presencial
- `VISIBLE_WEB` (Checkbox) - Para filtrar testimonios públicos

**Relaciones:**
- → CLIENTES (si DNI coincide)
- → EMPLEADOS (asesor calificado)

**Uso en Backend:**
- `backend/main.py` - Endpoints `/api/rating` (GET y POST)
- `backend/main.py` - Endpoint `/api/testimonios`

**Uso en Frontend:**
- `linktree/app.js:498-565` - Formulario de calificación
- `linktree/app.js:636-715` - Carrusel de testimonios

---

### 9. **LOGIN** (12 campos)
**Propósito:** Autenticación de usuarios (clientes y empleados)

**Campos:**
- `DNI`, `EMAIL`, `CONTRASEÑA` (hasheada)
- `ROL OPERATIVO` (Select): ADMIN, ASESOR, CLIENTE, SUPERVISOR
- `ESTADO DEL LOGIN` (Select): ACTIVO, INACTIVO, BLOQUEADO
- `TOKEN_SESION`, `FECHA_ULTIMO_LOGIN`

**Uso:**
- Portal de clientes (https://login-agentico-1770227340.surge.sh)
- **NO usado en linktree** (es portal público)

---

### 10. **Otras Tablas**
- **EMPLEADOS** (62 campos) - Staff, métricas de comisiones
- **OFICINAS** (41 campos) - Sucursales físicas
- **GESTIÓN GENERAL** (67 campos) - Cotizaciones, altas, anulaciones
- **COMPANIA** (13 campos) - Aseguradoras (Sancor, Rivadavia, etc.)
- **PRODUCTOS** (10 campos) - Tipos de seguros
- **PORTAL** (4 campos) - Config del portal web
- **Tokens** (5 campos) - JWT tokens
- **BIBLIOTECA_AUDIOS** (10 campos) - Audios de asistente de voz
- **TRAZABILIDAD/IA** (14 campos) - Logs de acciones IA
- **CARGA DE DOCUMENTOS** (9 campos) - Repositorio de archivos
- **PRIMA CALCULADA** (13 campos) - Cálculos de primas
- **Nueva Tabla** (11 campos) - ⚠️ Tabla sin nombre definido

---

## 🔗 MAPA DE RELACIONES ENTRE TABLAS

```
CLIENTES (centro neurálgico)
├── POLIZAS (1:N)
│   ├── COMPANIA (N:1)
│   └── PRODUCTOS (N:1)
├── DENUNCIA DE ACCIDENTE (1:N)
│   └── EMPLEADOS (N:1 - quien cargó)
├── DENUNCIA ROBO OC (1:N)
├── DENUNCIA ROBO / INCENDIO (1:N)
├── CALIFICACIONES (1:N)
├── GESTIÓN GENERAL (1:N)
│   ├── EMPLEADOS (N:1 - asesor)
│   └── OFICINAS (N:1)
└── EMPLEADOS (N:1 - asesor asignado)

CONFIG_FORMULARIOS
└── CONFIG_CAMPOS (1:N)

LOGIN
└── EMPLEADOS (1:1)
```

---

## 📝 FLUJO COMPLETO: Frontend → Backend → Airtable

### Ejemplo: Crear Denuncia de Choque

#### 1. **Frontend - Usuario completa formulario**
`linktree/index.html` línea 288-354
- Usuario hace click en "Reportar Siniestro"
- Paso 1: Valida DNI + Patente → `/api/validate-siniestro`
- Paso 2: Carga `FORM_CONFIG` → `/api/config-formularios`
- Paso 3: Selecciona tipo "choque"
- Paso 4: Renderiza form dinámico con campos de CONFIG_CAMPOS

#### 2. **Backend - Procesa validación**
`backend/main.py:564-643`
```python
@app.get("/api/validate-siniestro")
async def validate_siniestro(dni: str, patente: str):
    # Busca cliente por DNI
    table_clientes = get_table("CLIENTES")
    formula = f'({{DNI}} & "") = "{dni_limpio}"'
    records = table_clientes.all(formula=formula, max_records=1)

    # Obtiene compilación de pólizas (lookup)
    compilacion = cliente.get("ETIQUETA_POLIZA Compilación (de POLIZAS)", [])

    # Parsea texto con emojis para encontrar póliza de la patente
    # ⚠️ FRÁGIL - Depende de formato exacto
    for bloque in bloques_detectados:
        if patente_limpia in bloque.upper():
            return {"valid": True, "cliente": {...}, "poliza": {...}}
```

#### 3. **Backend - Sirve configuración**
`backend/main.py:721-796`
```python
@app.get("/api/config-formularios")
async def get_config_formularios():
    t_forms = get_table("CONFIG_FORMULARIOS")
    t_campos = get_table("CONFIG_CAMPOS")

    for f_rec in forms_records:
        codigo = f.get("CODIGO")
        visible = f.get("VISIBILIDAD", False)
        if not codigo or not visible: continue

        # Filtrar campos para este formulario
        my_fields = []
        for c_rec in campos_records:
            linked_forms = c.get("FORMULARIO")
            if form_id in linked_forms:
                campo_front = {
                    "id": c.get("ID CAMPO"),
                    "label": c.get("ETIQUETA"),
                    "type": c.get("TIPO"),
                    "required": c.get("OBLIGATORIO"),
                    "options": c.get("OPCIONES", "").split(",")
                }
                my_fields.append(campo_front)

        config_response[codigo] = {
            "titulo": f.get("TITULO"),
            "icono": f.get("ICONO"),
            "campos": my_fields
        }
```

#### 4. **Frontend - Submit formulario**
`linktree/app.js:1048-1129`
```javascript
async function handleSiniestroSubmit(e) {
    const formData = new FormData(form);
    const payload = new FormData();
    const datos = {};

    // Separar archivos de datos
    for (const [key, value] of formData.entries()) {
        if (value instanceof File && value.size > 0) {
            payload.append(key, value); // Archivo
        } else {
            datos[key] = value; // Dato de form
        }
    }

    payload.append('datos', JSON.stringify(datos));
    payload.append('tipo_formulario', 'choque');
    payload.append('poliza_record_id', polizaRecordId);

    // POST /api/create-siniestro
    const response = await fetch(BACKEND_CREATE_SINIESTRO, {
        method: 'POST',
        body: payload
    });
}
```

#### 5. **Backend - Procesa y crea registro**
`backend/main.py:841-1033`
```python
@app.post("/api/create-siniestro")
async def create_siniestro(request: Request):
    # 1. Parsear FormData
    form_data = await request.form()
    tipo_formulario = form_data.get("tipo_formulario")  # "choque"
    datos_json = form_data.get("datos")

    # 2. Subir archivos a Google Drive
    for key in form_data:
        for item in form_data.getlist(key):
            if isinstance(item, UploadFile):
                result = await upload_file_to_drive(item)
                archivos_subidos[key].append(result)

    # 3. Leer CONFIG_FORMULARIOS para obtener tabla destino
    form_record = t_forms.all(formula=f"{{CODIGO}} = '{tipo_formulario}'")[0]
    tabla_destino = form_record["fields"].get("TABLA RELACIONADA")
    # → "DENUNCIA DE ACCIDENTE"

    # 4. Leer CONFIG_CAMPOS para mapear IDs a columnas
    field_map = {}
    for c_rec in t_campos.all():
        if form_id in c_rec["fields"].get("FORMULARIO"):
            field_map[c["ID CAMPO"]] = c["COLUMNA AIRTABLE"]
    # → {"fecha_siniestro": "FECHA DEL SINIESTRO", "hora_siniestro": "HORA APROX. DEL SINIESTRO"}

    # 5. Construir payload Airtable
    airtable_payload = {}
    for campo_id, valor in datos_dict.items():
        if campo_id in field_map:
            airtable_payload[field_map[campo_id]] = valor

    # 6. Mapear archivos
    for campo_id, archivos in archivos_subidos.items():
        if campo_id in field_map:
            airtable_payload[field_map[campo_id]] = archivos  # Array de {url: "..."}

    # 7. Vincular póliza y cliente
    airtable_payload["POLIZAS"] = [poliza_record_id]
    airtable_payload["CLIENTE"] = [cliente_record_id]

    # 8. Agregar estado
    airtable_payload["ESTADO_WEB"] = "NUEVO WEB"  # ⚠️ Campo hardcodeado

    # 9. Crear registro en Airtable
    t_destino = get_table(tabla_destino)
    record = t_destino.create(airtable_payload, typecast=True)

    return {"status": "success", "id": record["id"]}
```

#### 6. **Airtable - Guarda registro**
- Se crea registro en tabla `DENUNCIA DE ACCIDENTE`
- Fórmula `ID_GESTION_UNICO` se calcula automáticamente
- Relaciones se vinculan por Record IDs
- Archivos se guardan como attachments (URLs de Google Drive)

---

## 🚨 PROBLEMAS IDENTIFICADOS Y SOLUCIONES

### 1. Campo `ESTADO_WEB` No Existe en Schema
**Ubicación:** `backend/main.py:981`
```python
airtable_payload["ESTADO_WEB"] = "NUEVO WEB"
```

**Problema:**
- Campo hardcodeado pero NO existe en ninguna tabla de denuncia
- Error: "Unknown field name: ESTADO_WEB"

**Solución:**
- **Opción A:** Crear campo `ESTADO_WEB` (Select) en las 3 tablas de denuncia
  - Opciones: NUEVO WEB, EN PROCESO, FINALIZADA, CERRADA
- **Opción B:** Usar campo existente `CLASIFICACIÓN` o similar
- **Opción C:** Eliminar esta línea si no es necesario

**Recomendación:** Opción A + agregar a CONFIG_CAMPOS para que sea editable

---

### 2. Validación Depende de Parsing de Texto con Emojis
**Ubicación:** `backend/main.py:620-678`

**Problema:**
- Campo `ETIQUETA_POLIZA Compilación` es un rollup de texto
- Se parsea buscando emojis (✅, ❌, ⏳, ⚠️) y keywords (VENCE, ANULADA)
- Si alguien cambia la fórmula en Airtable, todo se rompe

**Ejemplo de texto parseado:**
```
✅ VENCE 15/04/2026 | ABC123 | VOLKSWAGEN GOL | AUX INFINITY ❤️ VIDA
```

**Solución:**
- **Opción A (Ideal):** Cambiar relación CLIENTES → POLIZAS a directa
  - Endpoint: `GET /api/polizas-cliente?dni=12345678`
  - Retorna array JSON estructurado
  ```json
  [
    {
      "numero": "12345",
      "patente": "ABC123",
      "estado": "VIGENTE",
      "vencimiento": "2026-04-15",
      "marca": "VOLKSWAGEN",
      "modelo": "GOL",
      "auxilio": true,
      "vida": true
    }
  ]
  ```

- **Opción B (Rápida):** Agregar campo `PATENTE_NORMALIZADA` a POLIZAS
  - Fórmula: `UPPER(SUBSTITUTE(SUBSTITUTE({PATENTE DEL VEHICULO}, " ", ""), "-", ""))`
  - Buscar directamente en POLIZAS por DNI del cliente + patente

**Recomendación:** Opción B inmediata + planificar Opción A a futuro

---

### 3. Desacople en Tipos de Campos CONFIG_CAMPOS
**Ubicación:** Tabla CONFIG_CAMPOS, campo TIPO

**Problema:**
- Frontend espera: `"text"`, `"date"`, `"file"`, `"select"`
- Airtable tiene: `"Single line text (Texto de una línea)"`, `"Date (Fecha)"`
- Hay traducción manual necesaria

**Código afectado:**
`linktree/app.js:1001-1046` función `renderCampo()`
```javascript
switch(campo.type) {
    case 'file':   // ← Debe coincidir exactamente
    case 'select':
    case 'textarea':
    case 'text':
}
```

**Solución:**
- Cambiar opciones del campo TIPO en CONFIG_CAMPOS a valores técnicos:
  ```
  text → Texto simple
  textarea → Texto largo
  date → Fecha
  time → Hora
  number → Número
  file → Archivo adjunto
  select → Selección única
  ```

- Actualizar registros existentes

**Implementación:**
```python
# Script de migración
MAPEO = {
    "Single line text (Texto de una línea)": "text",
    "Long text (Texto largo)": "textarea",
    "Date (Fecha)": "date",
    "Attachment (Archivo adjunto)": "file",
    # etc...
}

for record in config_campos.all():
    tipo_actual = record['fields'].get('TIPO')
    if tipo_actual in MAPEO:
        config_campos.update(record['id'], {"TIPO": MAPEO[tipo_actual]})
```

---

### 4. No Hay Validación de Columnas en Tabla Destino
**Ubicación:** `backend/main.py:995-1024`

**Problema:**
- Si CONFIG_CAMPOS tiene typo en COLUMNA AIRTABLE, backend falla
- Error: `Unknown field name: FHEA_DEL_SINIESTRO` (typo de FECHA)
- Usuario final ve error genérico

**Ejemplo:**
```
CONFIG_CAMPOS:
- ID CAMPO: fecha_siniestro
- COLUMNA AIRTABLE: FHEA_DEL_SINIESTRO  ← TYPO!

Backend intenta:
airtable_payload["FHEA_DEL_SINIESTRO"] = "2026-03-03"

Airtable responde:
Error 422: Unknown field name: "FHEA_DEL_SINIESTRO"
```

**Solución:**
- Agregar validación al cargar configuración
```python
@app.get("/api/config-formularios")
async def get_config_formularios():
    # ... código existente ...

    # NUEVO: Validar que columnas existan
    errores = []
    for codigo, config in config_response.items():
        tabla_destino = form_records[codigo]["TABLA RELACIONADA"]
        t = get_table(tabla_destino)

        # Obtener nombres de campos reales
        sample = t.all(max_records=1)
        if sample:
            campos_reales = set(sample[0]['fields'].keys())

            for campo in config['campos']:
                columna = campo.get('columna_airtable')  # Exponerlo en API
                if columna and columna not in campos_reales:
                    errores.append(f"{codigo}.{campo['id']}: Campo '{columna}' no existe en {tabla_destino}")

    if errores:
        # Loggear pero no fallar (para no romper frontend)
        print(f"⚠️ ADVERTENCIAS DE CONFIGURACIÓN:\n" + "\n".join(errores))

    return config_response
```

---

### 5. Tablas de Denuncia Muy Grandes (152, 86, 86 campos)
**Problema:**
- DENUNCIA DE ACCIDENTE tiene 152 campos
- Muchos son lookups/rollups/fórmulas → queries lentas
- Difícil de mantener y entender

**Análisis:**
- ~30% son campos de datos
- ~40% son lookups/rollups
- ~30% son campos calculados/fórmulas

**Solución (Largo plazo):**
- Normalizar estructura
- Crear tablas secundarias:
  - `ARCHIVOS_SINIESTRO` (1:N con DENUNCIA)
  - `TERCEROS` (1:N con DENUNCIA) - Datos del otro vehículo
  - `SEGUIMIENTO` (1:N con DENUNCIA) - Timeline de estados

**Recomendación:** Mantener por ahora, refactorizar en fase 2

---

### 6. Campo `PLACEHOLDER` Faltante en CONFIG_CAMPOS
**Problema:**
- Frontend usa placeholder genérico
- No se puede personalizar por campo

**Solución:**
- Agregar campo `PLACEHOLDER` (Texto) a CONFIG_CAMPOS
- Actualizar endpoint para incluirlo en response
- Actualizar `renderCampo()` para usarlo

---

### 7. Sin Campo para Límite de Archivos
**Problema:**
- Todos los campos `type: file` aceptan múltiples archivos
- No hay forma de limitar cantidad o tamaño

**Solución:**
- Agregar a CONFIG_CAMPOS:
  - `MAX_ARCHIVOS` (Número) - Default: 5
  - `MAX_SIZE_MB` (Número) - Default: 10
  - `TIPOS_PERMITIDOS` (Texto) - Default: "image/jpeg,image/png,application/pdf"

---

## ✅ CAMPOS QUE FUNCIONAN CORRECTAMENTE

### Sistema CONFIG Dinámico
- ✅ CONFIG_FORMULARIOS define formularios
- ✅ CONFIG_CAMPOS define campos y mapeo
- ✅ Backend lee y sirve configuración
- ✅ Frontend renderiza dinámicamente
- ✅ Mapeo campo_id → columna_airtable funciona

### Validación de Cliente/Póliza
- ✅ Busca cliente por DNI
- ✅ Valida que tenga póliza activa
- ✅ Valida que patente coincida
- ✅ Retorna datos del cliente y póliza

### Upload de Archivos
- ✅ Archivos se suben a Google Drive
- ✅ URLs se guardan como attachments en Airtable
- ✅ Múltiples archivos por campo soportado

### Relaciones Entre Tablas
- ✅ CLIENTES vinculado a POLIZAS, DENUNCIAS, CALIFICACIONES
- ✅ EMPLEADOS vinculado a DENUNCIAS (quien cargó)
- ✅ POLIZAS vinculado a COMPANIA y PRODUCTOS

---

## 🎯 RECOMENDACIONES PRIORIZADAS

### 🔴 URGENTE (Esta Semana)

1. **Crear campo `ESTADO_WEB` en tablas de denuncia**
   - Tipo: Single Select
   - Opciones: NUEVO WEB, EN PROCESO, CONTACTADO, CERRADO
   - Agregar en: DENUNCIA DE ACCIDENTE, DENUNCIA ROBO OC, DENUNCIA ROBO / INCENDIO

2. **Agregar `PLACEHOLDER` a CONFIG_CAMPOS**
   - Actualizar schema
   - Modificar endpoint `/api/config-formularios`

3. **Normalizar tipos en CONFIG_CAMPOS**
   - Cambiar opciones de "Texto de una línea" a "text"
   - Ejecutar script de migración de registros existentes

4. **Agregar validación de columnas**
   - Implementar check de que columnas existan
   - Loggear advertencias en backend

### 🟠 IMPORTANTE (Este Mes)

5. **Crear campo `PATENTE_NORMALIZADA` en POLIZAS**
   - Fórmula: `UPPER(SUBSTITUTE(SUBSTITUTE({PATENTE DEL VEHICULO}, " ", ""), "-", ""))`
   - Usar en validación para evitar parsing

6. **Agregar campos de validación de archivos a CONFIG_CAMPOS**
   - MAX_ARCHIVOS, MAX_SIZE_MB, TIPOS_PERMITIDOS

7. **Crear endpoint `/api/polizas-cliente`**
   - Retorna JSON estructurado en lugar de texto parseado
   - Reemplaza parsing de ETIQUETA_POLIZA

8. **Documentar campos obligatorios**
   - Qué campos DEBE tener cada tabla de denuncia
   - Actualizar FULL_DB_SCHEMA.md

### 🟡 MEJORAS A FUTURO

9. **Refactorizar tablas de denuncia**
   - Separar en tablas más pequeñas
   - Eliminar campos duplicados legacy

10. **Agregar tabla de validación de formularios**
    - Ejecuta checks automáticos
    - Genera reportes de inconsistencias

---

## 📈 MÉTRICAS DEL SISTEMA

### Tamaño de Tablas
| Tabla | Campos | Relaciones | Fórmulas | Rollups |
|-------|--------|------------|----------|---------|
| DENUNCIA DE ACCIDENTE | 152 | 8 | ~30 | ~40 |
| DENUNCIA ROBO OC | 86 | 6 | ~20 | ~25 |
| DENUNCIA ROBO / INCENDIO | 86 | 6 | ~20 | ~25 |
| CLIENTES | 43 | 9 | 3 | 9 |
| POLIZAS | 40 | 12 | 2 | 4 |
| EMPLEADOS | 62 | 11 | 4 | 12 |
| GESTIÓN GENERAL | 67 | 8 | 8 | 15 |
| CONFIG_FORMULARIOS | 7 | 1 | 0 | 0 |
| CONFIG_CAMPOS | 8 | 1 | 0 | 0 |

### Endpoints Backend
| Endpoint | Método | Tabla(s) Usada(s) |
|----------|--------|-------------------|
| `/api/validate-siniestro` | GET | CLIENTES, (POLIZAS via lookup) |
| `/api/config-formularios` | GET | CONFIG_FORMULARIOS, CONFIG_CAMPOS |
| `/api/create-siniestro` | POST | CONFIG_FORMULARIOS, CONFIG_CAMPOS, DENUNCIA_* (dinámico) |
| `/api/rating` | GET/POST | CALIFICACIONES |
| `/api/testimonios` | GET | CALIFICACIONES (filtrado) |

---

## 🎓 CONCLUSIONES

### Lo Que Funciona Bien
1. ✅ Sistema de configuración dinámica es innovador y flexible
2. ✅ Relaciones entre tablas están bien diseñadas
3. ✅ Upload de archivos a Drive + vinculación funciona
4. ✅ Validación básica de cliente/póliza es sólida

### Lo Que Necesita Mejora Urgente
1. 🔴 Campo `ESTADO_WEB` faltante rompe creación de denuncias
2. 🔴 Parsing de pólizas es frágil y dependiente de formato
3. 🔴 Sin validación de que columnas CONFIG existan
4. 🔴 Tipos de campos desacopl ados entre frontend y backend

### Riesgos Principales
1. ⚠️ Cambio en fórmula ETIQUETA_POLIZA rompe validación
2. ⚠️ Typo en CONFIG_CAMPOS causa error confuso al usuario
3. ⚠️ Tablas muy grandes pueden tener performance issues

### Fortalezas del Diseño
1. 💪 Desacople frontend/backend mediante CONFIG
2. 💪 Escalable - agregar formularios sin tocar código
3. 💪 Trazabilidad completa (CLIENTES → POLIZAS → DENUNCIAS)

---

**Próximo paso sugerido:** Revisar este análisis con el equipo y priorizar fixes de los 4 problemas urgentes antes de agregar nuevas funcionalidades.
