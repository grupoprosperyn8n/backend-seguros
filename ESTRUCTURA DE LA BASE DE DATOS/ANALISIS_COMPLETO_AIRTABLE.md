# 📊 Análisis Completo de Airtable - Sistema de Seguros Agénticos

**Base ID:** `appuhslj3GFf60Tea`
**Fecha de Análisis:** 2026-03-03 11:44:56
**Total de Tablas:** 21

---

## 📑 Índice de Tablas

1. [CLIENTES](#clientes)
2. [EMPLEADOS](#empleados)
3. [OFICINAS](#oficinas)
4. [GESTIÓN GENERAL](#gestión-general)
5. [POLIZAS](#polizas)
6. [DENUNCIA DE ACCIDENTE](#denuncia-de-accidente)
7. [DENUNCIA ROBO OC](#denuncia-robo-oc)
8. [DENUNCIA ROBO / INCENDIO](#denuncia-robo-/-incendio)
9. [PRIMA CALCULADA](#prima-calculada)
10. [Nueva Tabla](#nueva-tabla)
11. [TRAZABILIDAD/IA](#trazabilidad/ia)
12. [CARGA DE DOCUMENTOS](#carga-de-documentos)
13. [COMPANIA](#compania)
14. [PRODUCTOS](#productos)
15. [LOGIN](#login)
16. [PORTAL](#portal)
17. [Tokens](#tokens)
18. [CALIFICACIONES](#calificaciones)
19. [BIBLIOTECA_AUDIOS](#biblioteca_audios)
20. [CONFIG_FORMULARIOS](#config_formularios)
21. [CONFIG_CAMPOS](#config_campos)

---

## 🗂️ CLIENTES

**ID:** `tblVAcMxNTLYXbLfT`  
**Total de Campos:** 43  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `NOMBRE NORMALIZADO` | Fórmula | Fórmula: `SUBSTITUTE(
  SUBSTITUTE(
    SUBSTITUTE(
      SU...` |
| `🏷️ ESTADO_CLIENTE` | Fórmula | Fórmula: `REGEX_REPLACE(
  TRIM(
    IF(
      {fldT7EQqT...` |
| `✅ CANTIDAD_POLIZAS` | Rollup (agregación) | Rollup: N/A |
| `🟢 POLIZAS_ACTIVAS` | Rollup (agregación) | Rollup: N/A |
| `🔴 POLIZAS_ANULADAS` | Rollup (agregación) | Rollup: N/A |
| `🟡 POLIZAS_EN_TRAMITES` | Rollup (agregación) | Rollup: N/A |
| `🟣 POLIZAS_SIN_VIGENCIA` | Rollup (agregación) | Rollup: N/A |
| `⭕ SIN_POLIZAS` | Rollup (agregación) | Rollup: N/A |
| `📆 LA_POLIZAS VENCE EN 30 DIAS` | Rollup (agregación) | Rollup: N/A |
| `📆 LA_POLIZAS VENCE EN 7 DIAS` | Rollup (agregación) | Rollup: N/A |
| `APELLIDO` | Texto (línea única) | - |
| `NOMBRES` | Texto (línea única) | - |
| `ID_UNICO_CLIENTE` | Fórmula | Fórmula: `"🆔 " & RIGHT(CONCATENATE({fldgfcpYGlVrRACcb}), 3) ...` |
| `DNI` | Número | - |
| `TELEFONO` | Teléfono | - |
| `EMAIL` | Email | - |
| `DIRECCION` | Desconocido (richText) | - |
| `FOTO PERFIL` | Archivos adjuntos | - |
| `CREADO X` | Selección única | Opciones: AGENTE IA, ASESOR |
| `EMPLEADOS` | Vínculo a registros | → EMPLEADOS |
| `NOTAS` | Desconocido (richText) | - |
| `FECHA DE ALTA` | Fecha de creación | - |
| `FECHA DE BAJA` | Fecha | - |
| `DENUNCIA DE ACCIDENTE` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `PRIMA CALCULADA` | Vínculo a registros | → PRIMA CALCULADA |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 6` | Vínculo a registros | → DENUNCIA ROBO OC |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `OFICINAS` | Vínculo a registros | → OFICINAS |
| `OFICINAS Compilación (de GESTIÓN GENERAL)` | Rollup (agregación) | Rollup: N/A |
| `OFICINAS Compilación (de CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))` | Rollup (agregación) | Rollup: N/A |
| `GESTIÓN GENERAL` | Vínculo a registros | → GESTIÓN GENERAL |
| `MOTIVOS DE LA CONSULTA Compilación (de GESTIÓN GENERAL)` | Desconocido (multipleLookupValues) | - |
| `TIPO DE PRODUCTOS (de GESTIÓN GENERAL)` | Desconocido (multipleLookupValues) | - |
| `COBERTURA (de GESTIÓN GENERAL)` | Desconocido (multipleLookupValues) | - |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL)` | Desconocido (multipleLookupValues) | - |
| `N° DE POLIZA (de GESTIÓN GENERAL)` | Desconocido (multipleLookupValues) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `ETIQUETA_POLIZA Compilación (de POLIZAS)` | Rollup (agregación) | Rollup: N/A |
| `ID_REGISTRO_CLIENTE` | Fórmula | Fórmula: `RECORD_ID()` |
| `IR A CLIENTE` | Botón | - |
| `CALIFICACIONES` | Vínculo a registros | → CALIFICACIONES |

### 🔗 Relaciones con Otras Tablas

- **EMPLEADOS** → `EMPLEADOS`
- **DENUNCIA DE ACCIDENTE** → `DENUNCIA DE ACCIDENTE`
- **PRIMA CALCULADA** → `PRIMA CALCULADA`
- **CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 6** → `DENUNCIA ROBO OC`
- **DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2** → `DENUNCIA ROBO / INCENDIO`
- **OFICINAS** → `OFICINAS`
- **GESTIÓN GENERAL** → `GESTIÓN GENERAL`
- **POLIZAS** → `POLIZAS`
- **CALIFICACIONES** → `CALIFICACIONES`

---

## 🗂️ EMPLEADOS

**ID:** `tblNbE8QOcNyutnbt`  
**Total de Campos:** 62  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `NOMBRE Y APELLIDO` | Texto (línea única) | - |
| `NOMBRE Y APELLIDO NORMALIZADO` | Fórmula | Fórmula: `UPPER({fldnLBeF1MB6KUdO4})` |
| `ID_UNICO_EMPLEADO` | Fórmula | Fórmula: `CONCATENATE(
  LEFT({fldnLBeF1MB6KUdO4}, 3),
  I...` |
| `CUIL` | Texto (línea única) | - |
| `DOMICILIO` | Texto (línea única) | - |
| `LOCALIDAD` | Texto (línea única) | - |
| `TELEFONO` | Teléfono | - |
| `EMAIL` | Email | - |
| `FECHA NAC.` | Fecha | - |
| `CUENTA` | Texto (línea única) | - |
| `INGRESO` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `BAJA` | Fecha | - |
| `FOTO DE PERFIL` | Archivos adjuntos | - |
| `Recuento (GESTION GENERAL)` | Conteo | - |
| `💰✅ TOTAL COMISIÓN FINAL Compilación (de GESTION GENERAL)` | Rollup (agregación) | Rollup: N/A |
| `Recuento (GESTION GENERAL) DEL AÑO` | Conteo | - |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) DEL AÑO` | Rollup (agregación) | Rollup: N/A |
| `Recuento (GESTION GENERAL)  MES EN CUSRSO` | Conteo | - |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) MES EN CURSO` | Rollup (agregación) | Rollup: N/A |
| `Recuento (GESTION GENERAL)  DE LA SEMANA` | Conteo | - |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) SEMANA EN CURSO` | Rollup (agregación) | Rollup: N/A |
| `Recuento (GESTION GENERAL)  ES HOY` | Conteo | - |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) ES HOY` | Rollup (agregación) | Rollup: N/A |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))TOTALES` | Conteo | - |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))DEL AÑO` | Conteo | - |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))MES CALENDARIO` | Conteo | - |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))SEMANA CALENDARIO` | Conteo | - |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))ES HOY` | Conteo | - |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ))TOTALES` | Conteo | - |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DEL AÑO` | Conteo | - |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DEL MES` | Conteo | - |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DE LA SEMANA` | Conteo | - |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DE HOY` | Conteo | - |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)` | Conteo | - |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)HOY` | Conteo | - |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)SEMANA` | Conteo | - |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)MES` | Conteo | - |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)AÑO` | Conteo | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `COMISIONES` | Texto (línea única) | - |
| `DENUNCIA DE ACCIDENTE` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `DENUNCIA ROBO OC` | Vínculo a registros | → DENUNCIA ROBO OC |
| `Resumen Total Anual` | Fórmula | Fórmula: `"TOTAL DE GESTION GENERAL ANUAL: " & {fldyRnnow5Qc...` |
| `COMISIONES MEJORADAS` | Texto (línea única) | - |
| `Login` | Vínculo a registros | → LOGIN |
| `CONTRASEÑA (from Login)` | Desconocido (multipleLookupValues) | - |
| `ROL OPERATIVO` | Desconocido (multipleLookupValues) | - |
| `ESTADO DEL LOGIN` | Desconocido (multipleLookupValues) | - |
| `GESTION GENERAL` | Vínculo a registros | → GESTIÓN GENERAL |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )` | Vínculo a registros | → DENUNCIA ROBO OC |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2` | Vínculo a registros | → DENUNCIA ROBO OC |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL)` | Desconocido (multipleLookupValues) | - |
| `🟠 ALERTA PAGO EN EFECTIVO (de GESTION GENERAL)` | Desconocido (multipleLookupValues) | - |
| `🔴 Aviso Comisión Cero (de GESTION GENERAL)` | Desconocido (multipleLookupValues) | - |
| `FECHA (de GESTION GENERAL)` | Desconocido (multipleLookupValues) | - |
| `CLIENTES` | Vínculo a registros | → CLIENTES |
| `CALIFICACIONES` | Vínculo a registros | → CALIFICACIONES |

### 🔗 Relaciones con Otras Tablas

- **DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL** → `DENUNCIA ROBO / INCENDIO`
- **DENUNCIA DE ACCIDENTE** → `DENUNCIA DE ACCIDENTE`
- **DENUNCIA ROBO OC** → `DENUNCIA ROBO OC`
- **Login** → `LOGIN`
- **GESTION GENERAL** → `GESTIÓN GENERAL`
- **CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2** → `DENUNCIA DE ACCIDENTE`
- **CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )** → `DENUNCIA DE ACCIDENTE`
- **CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )** → `DENUNCIA ROBO OC`
- **CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2** → `DENUNCIA ROBO OC`
- **DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2** → `DENUNCIA ROBO / INCENDIO`
- **CLIENTES** → `CLIENTES`
- **CALIFICACIONES** → `CALIFICACIONES`

---

## 🗂️ OFICINAS

**ID:** `tblDLIvG4bnW7UUMi`  
**Total de Campos:** 41  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `OFICINAS` | Texto (línea única) | - |
| `LOCALIDAD DE OFICINAS` | Texto (línea única) | - |
| `DOMICILIO` | Texto (línea única) | - |
| `TELEFONO` | Teléfono | - |
| `E-MAIL` | Email | - |
| `HORARIO` | Texto (línea única) | - |
| `GOOGLE MAP` | Botón | - |
| `GEOLOCALIZACION` | URL | - |
| `FOTO` | Archivos adjuntos | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  TOTAL` | Conteo | - |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  ANUAL` | Conteo | - |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  SEMANAL` | Conteo | - |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  MENSUAL` | Conteo | - |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE HOY` | Conteo | - |
| `CANTIDAD DE GESTIONES GENERALES TOTAL` | Conteo | - |
| `CANTIDAD DE GESTIONES GENERALES ANUAL` | Conteo | - |
| `CANTIDAD DE GESTIONES GENERALES MENSUAL` | Conteo | - |
| `CANTIDAD DE GESTIONES GENERALES SEMANAL` | Conteo | - |
| `CANTIDAD DE GESTIONES GENERALES HOY` | Conteo | - |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL  TOTAL` | Conteo | - |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL  ANUAL` | Conteo | - |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL MENSUAL` | Conteo | - |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL SEMANAL` | Conteo | - |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL HOY` | Conteo | - |
| `CANTIDAD CARGA DENUNCIA ROBO OC TOTAL` | Conteo | - |
| `CANTIDAD CARGA DENUNCIA ROBO OC ANUAL` | Conteo | - |
| `CANTIDAD CARGA DENUNCIA ROBO OC MENSUAL` | Conteo | - |
| `CANTIDAD CARGA DENUNCIA ROBO OC SEMANAL` | Conteo | - |
| `CANTIDAD CARGA DENUNCIA ROBO OC  HOY` | Conteo | - |
| `Resumen Cantidades y Total General` | Fórmula | Fórmula: `"TOTAL DE GESTION GENERAL: " & {fldgtOOZUgcMNz54c}...` |
| `CARGA DE DENUNCIA DE ACCIDENTE  MENSUAL` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )` | Vínculo a registros | → DENUNCIA ROBO OC |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2` | Vínculo a registros | → DENUNCIA ROBO OC |
| `GESTIÓN GENERAL 2` | Vínculo a registros | → GESTIÓN GENERAL |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 3` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 4` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `CLIENTES` | Texto (línea única) | - |
| `CLIENTES 2` | Vínculo a registros | → CLIENTES |

### 🔗 Relaciones con Otras Tablas

- **CARGA DE DENUNCIA DE ACCIDENTE  MENSUAL** → `DENUNCIA DE ACCIDENTE`
- **CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2** → `DENUNCIA DE ACCIDENTE`
- **CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )** → `DENUNCIA ROBO OC`
- **CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2** → `DENUNCIA ROBO OC`
- **GESTIÓN GENERAL 2** → `GESTIÓN GENERAL`
- **DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 3** → `DENUNCIA ROBO / INCENDIO`
- **DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 4** → `DENUNCIA ROBO / INCENDIO`
- **CLIENTES 2** → `CLIENTES`

---

## 🗂️ GESTIÓN GENERAL

**ID:** `tblA4AV8Lp7OvaUzI`  
**Total de Campos:** 67  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID_UNICO_GESTION` | Fórmula | Fórmula: `CONCATENATE({fld0wPLry103yD2Il}, "/", {fldkcOLXVUX...` |
| `CLIENTE` | Vínculo a registros | → CLIENTES |
| `DNI (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `EMAIL (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `OFICINAS` | Vínculo a registros | → OFICINAS |
| `ES CLIENTE` | Selección única | Opciones: No, Si |
| `MOTIVOS DE LA CONSULTA` | Selección única | Opciones: COTIZACIÓN, ALTAS, ANULACIÓN... |
| `TIPO DE PRODUCTOS` | Vínculo a registros | → PRODUCTOS |
| `TIPO ENDOSO / ANULACIÓN` | Selección única | Opciones: NO APLICA, ANULA POR MOTIVOS VS, DESESTIMA ASEGURADO... |
| `COBERTURA` | Selección única | Opciones: A, B, B1... |
| `FORMA DE PAGOS` | Selección única | Opciones: CREDITO, DEBITO, EFECTIVO... |
| `IMPORTE` | Moneda | - |
| `VIDA` | Selección única | Opciones: N CREDITO, No, Si |
| `IMPORTE VIDA` | Moneda | - |
| `AUXILIOS` | Selección única | Opciones: AUX 100, AUX 300, AUX 500... |
| `IMPORTE AUX 24` | Moneda | - |
| `ATENDIDO X` | Vínculo a registros | → EMPLEADOS |
| `Escribe tu ID` | Texto (línea única) | - |
| `TIPO DE ATENCIÓN` | Selección única | Opciones: AUTO-GESTIÓN, PRESENCIAL, WLVX... |
| `RECUPERO` | Selección única | Opciones: NO, SI |
| `RENOVACIÓN` | Selección única | Opciones: NO, SI |
| `DETALLAR OTROS` | Desconocido (richText) | - |
| `COMISIÓN VIDA` | Fórmula | Fórmula: `{fldm4h2HWbR0KUuiz}` |
| `💰 TOTAL COMISIÓN` | Fórmula | Fórmula: `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b...` |
| `💰✅ TOTAL COMISIÓN FINAL` | Fórmula | Fórmula: `IF({fldTukq50AVcZM8Eu} = 'N CREDITO', {fldFTtvSdMa...` |
| `🟠 ALERTA PAGO EN EFECTIVO` | Fórmula | Fórmula: `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', '🟠 Alerta: Pa...` |
| `🔴 Aviso Comisión Cero` | Fórmula | Fórmula: `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8E...` |
| `TIPO DE SOLICITUD` | Selección única | Opciones: COTIZACIÓN, ALTA PRODUCTO, DENUNCIA ACCIDENTE... |
| `ESTADO DE LA SOLICITUD` | Selección única | Opciones: NUEVA, EN PROCESO, FINALIZADA... |
| `FECHA DE SOLICITUD` | Fecha | - |
| `COMENTARIOS DEL CLIENTE` | Texto (multilínea) | - |
| `NOTIFICACIONES PORTAL CLIENTE` | Selección múltiple | Opciones: NUEVA SOLICITUD, SOLICITUD EN PROCESO, SOLICITUD FINALIZADA... |
| `DOCUMENTOS SOLICITADOS` | Archivos adjuntos | - |
| `datos adjunto portal cliente` | Archivos adjuntos | - |
| `ID_REGISTRO_CLIENTE_LOOKUP` | Desconocido (multipleLookupValues) | - |
| `IR A CLIENTE` | Botón | - |
| `COMISIONES MEJORADAS` | Texto (línea única) | - |
| `NUMERO` | Desconocido (autoNumber) | - |
| `FOTO PERFIL (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `ID_UNICO_CLIENTE` | Desconocido (multipleLookupValues) | - |
| `🔢✅ Cantidad de ALTAS` | Fórmula | Fórmula: `IF({fldQSvgctDcTZ9TXY} = 'ALTAS', 1, 0)` |
| `🔢 ❌ Cantidad de ANULACIÓN` | Fórmula | Fórmula: `IF({fldQSvgctDcTZ9TXY} = 'ANULACIÓN', 1, 0)` |
| `🔢 ✳️Diferencia ALTAS-ANULACIÓN` | Fórmula | Fórmula: `{fldSspNQJl5SPV40x} - {fld5oogxxETzlGnRg}` |
| `JAJAJA` | Fórmula | Fórmula: `IF(OR({fldi0omqIDbHpxO1O} > 0, {fld2b8cNvoIKGwsbt}...` |
| `💼 COMISIÓN VIDA + JAJAJA` | Fórmula | Fórmula: `{fldi0omqIDbHpxO1O} + {fldn734Iq6YJKVMV0}` |
| `COMISIÓN AUX` | Fórmula | Fórmula: `{fldtcTWSS2ffbzuZ7} / 2` |
| `COMISIÓN AUX + JAJAJA` | Fórmula | Fórmula: `{fld2b8cNvoIKGwsbt} + {fldn734Iq6YJKVMV0}` |
| `💵 COMISIÓN ALTA SIMPLE` | Fórmula | Fórmula: `{fldtCYI9REtFaInLB} * 0.02` |
| `💲 TOTAL COMI COMBINADAS` | Fórmula | Fórmula: `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b...` |
| `✅💰 TOTAL COMISIÓN FINAL 1` | Fórmula | Fórmula: `IF({fldQSvgctDcTZ9TXY} != 'ALTAS', 0, {fldanV8EbNt...` |
| `💰 TOTAL COMISIÓN AJUSTADA` | Fórmula | Fórmula: `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', 0, {fldmhPEfr...` |
| `Copia de 🔴 Aviso Comisión Cero` | Fórmula | Fórmula: `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8E...` |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )` | Texto (línea única) | - |
| `CLIENTES` | Texto (línea única) | - |
| `PATENTE DEL VEHICULO` | Texto (línea única) | - |
| `DENUNCIA DE ACCIDENTE` | Texto (línea única) | - |
| `DENUNCIA DE ACCIDENTE 2` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `MARCA` | Texto (línea única) | - |
| `MODELO` | Texto (línea única) | - |
| `AÑO DEL VEHICULO` | Número | - |
| `N° DE POLIZA` | Desconocido (multipleLookupValues) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `N°  POLIZA GESTIONADA` | Vínculo a registros | → POLIZAS |
| `COMPANIA` | Vínculo a registros | → COMPANIA |

### 🔗 Relaciones con Otras Tablas

- **CLIENTE** → `CLIENTES`
- **OFICINAS** → `OFICINAS`
- **TIPO DE PRODUCTOS** → `PRODUCTOS`
- **ATENDIDO X** → `EMPLEADOS`
- **DENUNCIA DE ACCIDENTE 2** → `DENUNCIA DE ACCIDENTE`
- **POLIZAS** → `POLIZAS`
- **N°  POLIZA GESTIONADA** → `POLIZAS`
- **COMPANIA** → `COMPANIA`

---

## 🗂️ POLIZAS

**ID:** `tblEpvdJAQCA7wUe9`  
**Total de Campos:** 40  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID_UNICO_GESTION` | Texto (línea única) | - |
| `FECHA VENCIMIENTO DE LA POLIZA` | Fecha | - |
| `ACTIVAR POLIZA` | Vínculo a registros | → GESTIÓN GENERAL |
| `ESTADO DE LA POLIZA` | Selección única | Opciones: ALTA , ANULACION, EN TRAMITE... |
| `N° DE POLIZA` | Texto (línea única) | - |
| `CLIENTES` | Texto (línea única) | - |
| `ARTICULO` | Texto (línea única) | - |
| `N° CERTIFICADO` | Texto (línea única) | - |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES)` | Texto (línea única) | - |
| `COBERTURA` | Selección única | Opciones: A, B, B4... |
| `MARCA DEL VEHICULO` | Texto (línea única) | - |
| `MODELO DEL VEHICULO` | Texto (línea única) | - |
| `AÑO DEL VEHICULO` | Número | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `COMISIONES MEJORADAS` | Texto (línea única) | - |
| `DENUNCIA ROBO / INCENDIO` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `GESTIÓN GENERAL` | Vínculo a registros | → GESTIÓN GENERAL |
| `CLIENTES 2` | Vínculo a registros | → CLIENTES |
| `DENUNCIA DE ACCIDENTE` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `DENUNCIA DE ACCIDENTE 2` | Vínculo a registros | → DENUNCIA DE ACCIDENTE |
| `TIPO DE COMBUSTIBLE` | Selección única | Opciones: NAFTA, GASOIL, GNC... |
| `USO DEL VEHICULO` | Texto (línea única) | - |
| `FECHA DE INICIO DE LA POLIZA` | Fecha | - |
| `ETIQUETA_POLIZA` | Fórmula | Fórmula: `UPPER(
  SWITCH(
    {fldkSsKEPwgEBkRQS},
    "...` |
| `VIDA` | Selección única | Opciones: Si, No, N CREDITO |
| `AUXILIO` | Selección única | Opciones: AUX, AUX 300, AUX 500... |
| `COMPANIA LINK` | Vínculo a registros | → COMPANIA |
| `EMAIL SINIESTROS (from COMPANIA LINK)` | Desconocido (multipleLookupValues) | - |
| `TEL. AUXILIO (from COMPANIA LINK)` | Desconocido (multipleLookupValues) | - |
| `LOGO (from COMPANIA LINK)` | Desconocido (multipleLookupValues) | - |
| `PRODUCTO LINK` | Vínculo a registros | → PRODUCTOS |
| `OFICINA` | Texto (línea única) | - |
| `COMISIONES` | Texto (línea única) | - |
| `DENUNCIA ROBO OC` | Texto (línea única) | - |
| `DENUNCIA ROBO OC 2` | Texto (línea única) | - |
| `DENUNCIA ROBO OC 3` | Vínculo a registros | → DENUNCIA ROBO OC |
| `DENUNCIA ROBO OC 4` | Vínculo a registros | → DENUNCIA ROBO OC |
| `DENUNCIA ROBO OC 5` | Vínculo a registros | → DENUNCIA ROBO OC |
| `DENUNCIA ROBO / INCENDIO 2` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |

### 🔗 Relaciones con Otras Tablas

- **ACTIVAR POLIZA** → `GESTIÓN GENERAL`
- **DENUNCIA ROBO / INCENDIO** → `DENUNCIA ROBO / INCENDIO`
- **GESTIÓN GENERAL** → `GESTIÓN GENERAL`
- **CLIENTES 2** → `CLIENTES`
- **DENUNCIA DE ACCIDENTE** → `DENUNCIA DE ACCIDENTE`
- **DENUNCIA DE ACCIDENTE 2** → `DENUNCIA DE ACCIDENTE`
- **COMPANIA LINK** → `COMPANIA`
- **PRODUCTO LINK** → `PRODUCTOS`
- **DENUNCIA ROBO OC 3** → `DENUNCIA ROBO OC`
- **DENUNCIA ROBO OC 4** → `DENUNCIA ROBO OC`
- **DENUNCIA ROBO OC 5** → `DENUNCIA ROBO OC`
- **DENUNCIA ROBO / INCENDIO 2** → `DENUNCIA ROBO / INCENDIO`

---

## 🗂️ DENUNCIA DE ACCIDENTE

**ID:** `tbl4570W1T0qGdj8w`  
**Total de Campos:** 152  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID_GESTION_UNICO` | Fórmula | Fórmula: `CONCATENATE(
  ARRAYJOIN({fldLrTr9OUePj5eER}, ""),...` |
| `FECHA CARGA` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `ESCRIBE TÚ ID` | Texto (línea única) | - |
| `ATENDIDO X` | Vínculo a registros | → EMPLEADOS |
| `OFICINAS` | Vínculo a registros | → OFICINAS |
| `TIPO DE ATENCIÓN` | Selección única | Opciones: WLVX, PRESENCIAL, WAPP-PERSONAL... |
| `MOTIVOS DE LA CONSULTA` | Selección única | Opciones: SINIESTRO |
| `TIPO DE PRODUCTOS` | Desconocido (multipleLookupValues) | - |
| `ID_UNICO_CLIENTE` | Desconocido (multipleLookupValues) | - |
| `CLIENTE` | Vínculo a registros | → CLIENTES |
| `DNI (de CLIENTES)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO (de CLIENTES)` | Desconocido (multipleLookupValues) | - |
| `EMAIL (de CLIENTES)` | Desconocido (multipleLookupValues) | - |
| `MARCA DEL VEHICULO` | Texto (línea única) | - |
| `MODELO DEL  VEHICULO` | Texto (línea única) | - |
| `AÑO DEL VEHICULO` | Selección única | Opciones: 1975, 1982, 1971... |
| `CARGADO EN CIA X` | Vínculo a registros | → EMPLEADOS |
| `N° DE POLIZA Compilación (de POLIZAS 2)` | Rollup (agregación) | Rollup: N/A |
| `MARCA (from NUMERO DE POLIZA)` | Rollup (agregación) | Rollup: N/A |
| `MODELO DEL VEHICULO Compilación (de POLIZAS 2)` | Rollup (agregación) | Rollup: N/A |
| `AÑO DEL VEHICULO (from NUMERO DE POLIZA)` | Rollup (agregación) | Rollup: N/A |
| `PATENTE DEL VEHICULO` | Rollup (agregación) | Rollup: N/A |
| `COBERTURA` | Rollup (agregación) | Rollup: N/A |
| `CODIGO EMISION DE LA POLIZA` | Vínculo a registros | → OFICINAS |
| `ARTICULO` | Número | - |
| `NUMERO DE CERTIFICADO` | Número | - |
| `PARTES AFECTADAS` | Selección múltiple | Opciones: PARTE DELANTERA, LATERALES, PARTE TRASERA... |
| `FECHA DEL SINIESTRO` | Fecha | - |
| `HORA APROX. DEL SINIESTRO` | Duración | - |
| `LUGAR O ESTABLECIMIENTO` | Texto (multilínea) | - |
| `DIRECCIÓN Y N°` | Texto (multilínea) | - |
| `INTERSECCIÓN O ENTRE CALLES` | Texto (multilínea) | - |
| `LOCALIDAD / PROV. / PAIS` | Texto (multilínea) | - |
| `GOOGLE  MAPS URL` | Desconocido (aiText) | - |
| `CODIGO POSTAL` | Texto (línea única) | - |
| `TIPO DE CALLE` | Selección única | Opciones: BOCACALLE, CALLE, RUTA... |
| `NOMBRE Y APELLIDO ( COND )` | Texto (línea única) | - |
| `DNI ( COND )` | Número | - |
| `DOMICILIO ( COND )` | Texto (línea única) | - |
| `TELEFONO ( COND )` | Teléfono | - |
| `FECHA DE NACIMIENTO (COND)` | Fecha | - |
| `ESTADO CIVIL (COND)` | Selección única | Opciones: CASADO, SOLTERO, SEPARADO/A... |
| `RELACIÓN CON EL ASEGURADO` | Texto (línea única) | - |
| `ALCOHOLEMIA DEL CONDUCTOR` | Selección única | Opciones: RESULTADO POSITIVO, RESULTADO NEGATIVO, SE NEGO... |
| `TIPO DE CONDUCTOR` | Selección única | Opciones: HABITUAL, NO HABITUAL, NINGUNO |
| `LICENCIA CONDUCIR (COND)` | Número | - |
| `EMISOR DE LICENCIA (COND)` | Desconocido (richText) | - |
| `FECHA EMISIÓN (COND)` | Fecha | - |
| `FECHA VENCIMIENTO (COND)` | Fecha | - |
| `CATEGORIAS (COND)` | Desconocido (richText) | - |
| `NOMBRE Y APELLIDO ( TER 1 )` | Texto (línea única) | - |
| `DNI ( TER 1 )` | Número | - |
| `TELEFONO ( TER 1 )` | Teléfono | - |
| `MARCA DEL VEHICULO  ( TER 1 )` | Texto (línea única) | - |
| `MODELO DEL VEHICULO ( TER 1 )` | Texto (línea única) | - |
| `PATENTE ( TER 1 )` | Texto (línea única) | - |
| `COMPAÑIA DE SEGURO ( TER 1 )` | Selección única | Opciones: , ACA, AGRO SALTA... |
| `CLASIFICACIÓN DEL TERCERO ( TER 1 )` | Selección única | Opciones: BICICLETA , PEATON, SIN DATOS DEL SEGURO... |
| `HUBO DAÑOS A COSAS DE TERCERO (TER 1)` | Selección única | Opciones: SI, NO |
| `HABIA ACOMPAÑANTES (TER 1)` | Selección única | Opciones: SI, NO |
| `AFIRMATIVO - NOMBRE APELLIDO Y DNI DE LOS ACOMPAÑANTES (TER1)` | Desconocido (richText) | - |
| `PRODUCTO LINK (de POLIZAS 2)` | Rollup (agregación) | Rollup: N/A |
| `NOMBRE Y APELLIDO ( TER 2 )` | Texto (línea única) | - |
| `DNI ( TER 2 )` | Número | - |
| `TELEFONO ( TER 2 )` | Teléfono | - |
| `MARCA DEL VEHICULO ( TER 2 )` | Texto (línea única) | - |
| `MODELO DEL VEHICULO ( TER 2 )` | Texto (línea única) | - |
| `PATENTE ( TER 2 )` | Texto (línea única) | - |
| `COMPAÑIA DE SEGURO  ( TER 2 )` | Selección única | Opciones: , ACA, AGROSALTA... |
| `CLASIFICACIÓN DEL TERCERO ( TER 2 )` | Selección única | Opciones: BICICLETA, PEATON, SIN DATOS DEL SEGURO... |
| `HUBO DAÑOS A COSAS DE TERCERO (TER 2)` | Selección única | Opciones: SI, NO |
| `HABIA ACOMPAÑANTES (TER 2)` | Selección única | Opciones: SI, NO |
| `AFIRMATIVO - NOMBRE APELLIDO Y DNI DE LOS ACOMPAÑANTES (TER2)` | Desconocido (richText) | - |
| `RELATOS DEL HECHO` | Texto (multilínea) | - |
| `TIPO DE CALZADA` | Selección única | Opciones: PAVIMENTADA, TIERRA, NINGUNO... |
| `ESTADO DE CALZADA` | Selección única | Opciones: BUENO, REGULAR, MALO... |
| `ESTADO DEL TIEMPO` | Selección única | Opciones: SECO, LLUVIA, NIEBLA... |
| `SENTIDO DE CIRCULACION` | Selección única | Opciones: ESTACIONADO, NORTE - SUR, SUR - NORTE... |
| `HUBO IMPACTO` | Selección única | Opciones: SI, NO |
| `SENTIDO CIRCULACIÓN DEL OTRO VEHICULO` | Selección única | Opciones: ESTACIONADO, NORTE - SUR, SUR - NORTE... |
| `SEÑALES DE TRANSITO` | Selección única | Opciones: CARTELES, VALLADO, REDUCTORES... |
| `HABIA SEMAFOROS` | Selección múltiple | Opciones: SI, NO, VERDE... |
| `DISTANCIA ENTRE VEHICULOS (METROS)` | Selección única | Opciones: 1 METRO, 2 METROS, 3 METROS... |
| `PERSONAS EN VEHICULO (INCLUIDO CONDUCTOR)` | Selección única | Opciones: 1, 2, 3... |
| `TIPO DE COMBUSTIBLE` | Selección única | Opciones: GNC, NAFTA, GASOIL... |
| `USO DEL VEHICULO` | Selección única | Opciones: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES... |
| `TESTIGOS PRESENTES EN EL MOMENTO DEL HECHO` | Selección única | Opciones: SI, NO |
| `DATOS TESTIGOS - NOMBRE Y APELLIDO` | Texto (línea única) | - |
| `DNI DEL TESTIGO` | Número | - |
| `DATOS TESTIGOS - DOMICILIO` | Texto (línea única) | - |
| `DATOS TESTIGOS - TELEFONO` | Teléfono | - |
| `DENUNCIA ANTE AUTORIDAD` | Selección única | Opciones: SI, NO |
| `CLASIFICACIÓN` | Selección única | Opciones: CON LESIONES, SIN LESIONES, GRANIZO... |
| `NOMBRE Y APELLIDO DEL LESIONADO` | Texto (línea única) | - |
| `DNI DEL LESIONADO` | Texto (línea única) | - |
| `LESION MORTAL` | Selección única | Opciones: SI, NO |
| `TRASLADO POR MEDIOS PROPIOS` | Selección única | Opciones: SI, NO |
| `MEDIO DE  TRASLADO` | Selección única | Opciones: AMBULANCIA, VEHICULO PARTICULAR, NINGUNO |
| `CENTRO DE INTERNACION` | Texto (multilínea) | - |
| `ESTA INTERNADO` | Selección única | Opciones: NO, SI |
| `DESCRIPCIÓN DE LESIONES` | Texto (multilínea) | - |
| `FOTO DNI AMBOS LADOS` | Archivos adjuntos | - |
| `FOTO CEDULA VERDE AMBOS LADOS` | Archivos adjuntos | - |
| `FOTO CARNET CONDUCIR AMBOS LADOS` | Archivos adjuntos | - |
| `FOTO DAÑO DEL VEHICULO X 3` | Archivos adjuntos | - |
| `FOTO DE DENUNCIA OFICIAL ( EN CASO DE LESIONES )` | Archivos adjuntos | - |
| `RAZÓN SOCIAL DEL TALLER (T. RIESGO)` | Texto (línea única) | - |
| `DOMICILIO TALLER (T. RIESGO)` | Texto (línea única) | - |
| `TELEFONO TALLER (T. RIESGO)` | Teléfono | - |
| `CULPABILIDAD IA` | Desconocido (aiText) | - |
| `AGENTE 2: GESTOR DE PROTOCOLO` | Desconocido (aiText) | - |
| `TRATAMIENTO` | Selección única | Opciones: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO -A LA ESPERA DE RESPUESTA... |
| `ESTADO DEL RECLAMOS` | Selección única | Opciones: RESUELVE CON ABOGADO PERSONAL, RESUELVE CON ABOGADO NUESTRO, RESUELVE CON TALLER... |
| `OBSERVACIONES (DESTRUCCION TOTAL DETALLAR)` | Desconocido (richText) | - |
| `NUMERO DE SINIESTRO` | Texto (línea única) | - |
| `Estado_Gestion_AI` | Selección única | Opciones: Nuevo, Formulario Enviado, Pendiente... |
| `Fecha_Derivacion` | Fecha y hora | - |
| `Documentos_Pendientes` | Desconocido (richText) | - |
| `Historial_Chat_AI` | Texto (multilínea) | - |
| `URL_Audio` | URL | - |
| `Transcripcion_Audio` | Texto (multilínea) | - |
| `Chat_ID` | Texto (línea única) | - |
| `Carga de Documentos` | Texto (línea única) | - |
| `FOTO PERFIL (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `Checklist de documentación` | Selección múltiple | Opciones: Denuncia policial, Copia DNI, Fotos del vehículo... |
| `Estado del trámite` | Selección única | Opciones: Iniciado, En proceso, Documentación completa... |
| `Fecha de última actualización` | Fecha y hora | - |
| `Notas de seguimiento` | Texto (multilínea) | - |
| `Responsable del seguimiento` | Vínculo a registros | → EMPLEADOS |
| `datos adjunto portal cliente` | Archivos adjuntos | - |
| `ID_REGISTRO_CLIENTE_LOOKUP` | Desconocido (multipleLookupValues) | - |
| `IR A CLIENTE` | Botón | - |
| `ESTADO_WEB` | Selección única | Opciones: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `ID-GESTION-UNICO` | Texto (línea única) | - |
| `NUMERO ID AUTOMATICO` | Desconocido (autoNumber) | - |
| `CULPABILIDAD` | Selección única | Opciones: CULPABLE, NO CULPABLE, VER TENGO DUDAS... |
| `back uu CULPABILIDAD IA` | Desconocido (aiText) | - |
| `Copia de CULPABILIDAD IA` | Desconocido (aiText) | - |
| `Código` | Texto (multilínea) | - |
| `GESTIÓN GENERAL 2` | Vínculo a registros | → GESTIÓN GENERAL |
| `ID_UNICO_GESTION (from GESTIÓN GENERAL 2)` | Desconocido (multipleLookupValues) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `CLIENTES 2 (from POLIZAS)` | Desconocido (multipleLookupValues) | - |
| `POLIZAS 2` | Vínculo a registros | → POLIZAS |
| `N° CERTIFICADO (from POLIZAS 2)` | Desconocido (multipleLookupValues) | - |
| `MARCA (from POLIZAS 2)` | Desconocido (multipleLookupValues) | - |
| `MODELO (from POLIZAS 2)` | Desconocido (multipleLookupValues) | - |
| `AÑO DEL VEHICULO (from POLIZAS 2)` | Desconocido (multipleLookupValues) | - |
| `Seleccionar` | Selección única | Opciones: ES EL ASEGURADO, NO ES EL ASEGURADO |
| `Creado por` | Creado por | - |

### 🔗 Relaciones con Otras Tablas

- **ATENDIDO X** → `EMPLEADOS`
- **OFICINAS** → `OFICINAS`
- **CLIENTE** → `CLIENTES`
- **CARGADO EN CIA X** → `EMPLEADOS`
- **CODIGO EMISION DE LA POLIZA** → `OFICINAS`
- **Responsable del seguimiento** → `EMPLEADOS`
- **GESTIÓN GENERAL 2** → `GESTIÓN GENERAL`
- **POLIZAS** → `POLIZAS`
- **POLIZAS 2** → `POLIZAS`

---

## 🗂️ DENUNCIA ROBO OC

**ID:** `tblRsZQhnNdJqnxf8`  
**Total de Campos:** 86  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID_UNICO_GESTION` | Fórmula | Fórmula: `{fldnO2OVcgjrkhqxZ} & "/" & {fldHUZWssgXc9qrIu} & ...` |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `ESCRIBE TÚ ID` | Texto (línea única) | - |
| `ATENDIDO X` | Vínculo a registros | → EMPLEADOS |
| `CARGADA EN CIA X` | Vínculo a registros | → EMPLEADOS |
| `OFICINAS` | Vínculo a registros | → OFICINAS |
| `TIPO DE ATENCIÓN` | Selección única | Opciones: PRESENCIAL, WAPP-PERSONAL, 0810-AUTO-GESTIÓN... |
| `MOTIVOS DE LA CONSULTA` | Selección única | Opciones: SINIESTRO, NO SINIESTRO |
| `PRODUCTO` | Desconocido (multipleLookupValues) | - |
| `TIPO DE PRODUCTOS` | Rollup (agregación) | Rollup: N/A |
| `CLIENTE` | Vínculo a registros | → CLIENTES |
| `DNI (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO  CLIENTE` | Desconocido (multipleLookupValues) | - |
| `EMAIL CLIENTE` | Desconocido (multipleLookupValues) | - |
| `MARCA DEL VEHICULO Compilación (de N° POLIZA)` | Rollup (agregación) | Rollup: N/A |
| `MODELO DEL VEHICULO` | Rollup (agregación) | Rollup: N/A |
| `AÑO DEL VEHICULO` | Rollup (agregación) | Rollup: N/A |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES) Compilación (de N° POLIZA)` | Rollup (agregación) | Rollup: N/A |
| `COBERTURA` | Rollup (agregación) | Rollup: N/A |
| `CLASIFICACIÓN DE ADICIONALES` | Selección única | Opciones: CON ADICIONAL CRISTALES, YA INCLUYE EN COBERTURA, CON ADICIONAL CUBIERTAS... |
| `ALCANCE DE COBERTURA` | Selección única | Opciones: ESTÁ CUBIERTO, NO ESTÁ CUBIERTO |
| `CÓDIGO EMISÍON DE PÓLIZA` | Vínculo a registros | → OFICINAS |
| `ARTICULO` | Rollup (agregación) | Rollup: N/A |
| `CERTIFICADO` | Rollup (agregación) | Rollup: N/A |
| `FECHA DEL SINIESTRO` | Fecha | - |
| `HORA APROX. DEL SINIESTRO` | Duración | - |
| `LUGAR O ESTABLECIMIENTO` | Desconocido (richText) | - |
| `INTERSECCIÓN O ENTRE CALLES` | Texto (multilínea) | - |
| `LOCALIDAD / PROV. / PAIS` | Texto (multilínea) | - |
| `CÓDIGO POSTAL` | Texto (línea única) | - |
| `Google Maps URL` | Desconocido (aiText) | - |
| `N° POLIZA` | Vínculo a registros | → POLIZAS |
| `N° DE POLIZA` | Rollup (agregación) | Rollup: N/A |
| `ID_UNICO_CLIENTE` | Desconocido (multipleLookupValues) | - |
| `DIRECCIÓN Y N°` | Texto (línea única) | - |
| `NOMBRE Y APELLIDO ( DENU )` | Texto (línea única) | - |
| `DNI ( DENU )` | Número | - |
| `TELEFONO ( DENU )` | Teléfono | - |
| `DOMICILIO ( DENU )` | Texto (multilínea) | - |
| `FECHA DE NACIMIENTO (DENU)` | Fecha | - |
| `ESTADO CIVIL ( DENU )` | Texto (línea única) | - |
| `RELACIÓN CON EL ASEGURADO` | Texto (línea única) | - |
| `RELATOS DEL HECHO` | Texto (multilínea) | - |
| `CLASIFICACIÓN DEL DAÑO` | Selección múltiple | Opciones: PARABRISAS, LUNETA TRASERA, LATERAL DELANTERO... |
| `DEJA CON FRECUENCIA VEHÍCULO AQUÍ` | Selección única | Opciones: SÍ, NO |
| `TENÍA ALARMA ACTIVADA` | Selección única | Opciones: SÍ, NO, NO TIENE ALARMA |
| `USO DEL VEHÍCULO` | Selección única | Opciones: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES... |
| `TIPO DE LUGAR` | Selección única | Opciones: PÚBLICO, PRIVADO |
| `TIENE CÁMARA DE SEGURIDAD` | Selección única | Opciones: SÍ, NO |
| `HUBO TESTIGOS` | Selección única | Opciones: SÍ, NO |
| `CANTIDAD DE RUEDAS ROBADAS` | Selección única | Opciones: 1, 2, 3... |
| `REALIZÓ LLAMADO AL 911` | Selección única | Opciones: SÍ, NO |
| `REALIZÓ DENUNCIA POLICIAL` | Selección única | Opciones: SÍ, NO |
| `FRECUENCIA DE USO DEL VEHÍCULO` | Selección única | Opciones: DIARIO, VARIOS DÍAS POR SEMANA, UNA VEZ POR SEMANA... |
| `FOTO DNI` | Archivos adjuntos | - |
| `FOTO CEDULA VERDE` | Archivos adjuntos | - |
| `FOTO CARNET CONDUCIR` | Archivos adjuntos | - |
| `FOTO DAÑO DEL VEHICULO` | Archivos adjuntos | - |
| `FOTO DE DENUNCIA OFICIAL ( EN CASO DE ROBO )` | Archivos adjuntos | - |
| `FOTO DE DENUNCIA OFICIAL` | Archivos adjuntos | - |
| `FOTO FACTURA COMPRA DE BATERÍA ( EN CASO ROBO BATERÍA )` | Archivos adjuntos | - |
| `NUMERO DE SINIESTRO ` | Texto (línea única) | - |
| `OBSERVACIONES` | Texto (multilínea) | - |
| `ORDEN PEDIDA A CIA` | Selección única | Opciones: SI, NO |
| `VERIFICACION DE ORDEN` | Selección única | Opciones: ENVIADA AL ASEGURADO, NO LE LLEGO, SE LLAMO AL ASEGURADO... |
| `Checklist de documentación` | Selección múltiple | Opciones: DNI, Título de propiedad, Denuncia policial... |
| `Estado del trámite` | Selección única | Opciones: Nuevo, En revisión, Enviado a compañía... |
| `Fecha de última actualización` | Fecha y hora | - |
| `Notas de seguimiento` | Texto (multilínea) | - |
| `Responsable del seguimiento` | Vínculo a registros | → EMPLEADOS |
| `datos adjunto portal cliente` | Archivos adjuntos | - |
| `NOMBRE Y APELLIDO TESTIGO` | Texto (línea única) | - |
| `DNI TESTIGO` | Número | - |
| `DOMICILIO DEL TESTIGO` | Texto (multilínea) | - |
| `TELEFONO TESTIGO` | Teléfono | - |
| `TIPO DE CONSULTA` | Selección múltiple | Opciones: ROBO DE BATERÍA, ROBO DE AUTO, ROBO DE ACCESORIOS... |
| `TRATAMIENTO` | Selección única | Opciones: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO -A LA ESPERA DE RESPUESTA... |
| `IR A CLIENTE` | Botón | - |
| `ID_REGISTRO_CLIENTE_LOOKUP` | Desconocido (multipleLookupValues) | - |
| `ESTADO_WEB` | Selección única | Opciones: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `NUMERO` | Desconocido (autoNumber) | - |
| `From field: N° POLIZA` | Texto (línea única) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `POLIZAS 2` | Vínculo a registros | → POLIZAS |
| `PRODUCTO LINK (de POLIZAS 2)` | Desconocido (multipleLookupValues) | - |

### 🔗 Relaciones con Otras Tablas

- **ATENDIDO X** → `EMPLEADOS`
- **CARGADA EN CIA X** → `EMPLEADOS`
- **OFICINAS** → `OFICINAS`
- **CLIENTE** → `CLIENTES`
- **CÓDIGO EMISÍON DE PÓLIZA** → `OFICINAS`
- **N° POLIZA** → `POLIZAS`
- **Responsable del seguimiento** → `EMPLEADOS`
- **POLIZAS** → `POLIZAS`
- **POLIZAS 2** → `POLIZAS`

---

## 🗂️ DENUNCIA ROBO / INCENDIO

**ID:** `tblLnVFRONjVZ7YUH`  
**Total de Campos:** 86  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `Código` | Fórmula | Fórmula: `CONCATENATE({fld0OBwDwHzdrkLgg}, "/", {fldd7FgvlOD...` |
| `IR A CLIENTE` | Botón | - |
| `ESCRIBE TÚ ID` | Texto (línea única) | - |
| `ATENDIDO X` | Vínculo a registros | → EMPLEADOS |
| `OFICINAS` | Vínculo a registros | → OFICINAS |
| `TIPO DE ATENCIÓN` | Selección única | Opciones: WAPP-PERSONAL, PRESENCIAL, 0810-AUTO-GESTIÓN... |
| `MOTIVOS DE LA CONSULTA` | Selección única | Opciones: SINIESTRO |
| `TIPO DE PRODUCTOS` | Selección única | Opciones: MOTO, AUTO, REMIS... |
| `CARGADO EN CIA X` | Vínculo a registros | → EMPLEADOS |
| `ID_UNICO_CLIENTE` | Desconocido (multipleLookupValues) | - |
| `CLIENTE` | Vínculo a registros | → CLIENTES |
| `DNI (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `EMAIL (from CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `MARCA DEL VEHICULO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `MODELO DEL VEHICULO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `AÑO DEL VEHICULO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `PATENTE DEL VEHICULO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `COBERTURA (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `ALCANCE DE COBERTURA` | Selección única | Opciones: ESTA CUBIERTO, NO ESTA CUBIERTO |
| `CÓDIGO EMISÍON DE PÓLIZA` | Vínculo a registros | → OFICINAS |
| `ARTICULO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `CERTIFICADO (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `FECHA DEL SINIESTRO` | Fecha | - |
| `HORA APROX.DELSINIESTRO` | Duración | - |
| `DIRECCIÓN Y N°` | Texto (línea única) | - |
| `LUGAR O ESTABLECIMIENTO` | Texto (multilínea) | - |
| `INTERSECCIÓN O ENTRE CALLES` | Texto (multilínea) | - |
| `LOCALIDAD / PROV. / PAIS` | Texto (multilínea) | - |
| `CÓDIGO POSTAL` | Texto (línea única) | - |
| `Google Maps URL` | Desconocido (aiText) | - |
| `NOMBRE Y APELLIDO ( DENU )` | Texto (línea única) | - |
| `DNI ( DENU )` | Número | - |
| `TELEFONO ( DENU )` | Teléfono | - |
| `DOMICILIO ( DENU )` | Texto (línea única) | - |
| `FECHA DE NACIMIENTO` | Fecha | - |
| `ESTADO CIVIL` | Selección única | Opciones: CONCUBINATO, SOLTERO, CASADO... |
| `RELACIÓN CON EL ASEGURADO` | Texto (línea única) | - |
| `RELATOS DEL HECHO` | Texto (multilínea) | - |
| `CLASIFICACIÓN DEL SINIESTRO` | Selección única | Opciones: ROBO TOTAL, INCENDIO PARCIAL, DESTRUCCIÓN TOTAL... |
| `ROBO TOTAL (HALLAZGO)` | Selección única | Opciones: SI, NO |
| `INCENDIO (INTERVENCIÓN BOMBEROS)` | Selección única | Opciones: SI, NO |
| `SINIESTRO (FUERZA MAYOR)` | Selección única | Opciones: SI, NO |
| `AFIRMATIVO (DESCRIBIR)` | Texto (multilínea) | - |
| `USO DEL VEHICULO` | Selección única | Opciones: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES... |
| `DAÑOS A  TERCEROS` | Selección única | Opciones: SI, NO |
| `AFIRMATIVO (Nombre, Apellido, DNI)` | Texto (multilínea) | - |
| `HUBO LESIONADOS` | Selección única | Opciones: SI, NO |
| `AFIRMATIVO LESIONADOS (Nombre, Apellido, DNI)` | Texto (multilínea) | - |
| `LESION MORTAL` | Selección única | Opciones: SI, NO |
| `SE RETIRO POR MEDIOS PROPIOS` | Selección única | Opciones: SI, NO |
| `COMO FUE TRASLADADO` | Selección única | Opciones: AMULANCIA, VEHICULO PARTICULAR, NINGUNO |
| `SE ENCUENTRA INTERNADO` | Selección única | Opciones: SI, NO |
| `CENTRO DE INTERNACIÓN` | Texto (multilínea) | - |
| `DESCRIPCIÓN DE LA LESIÓN` | Texto (multilínea) | - |
| `FOTO DNI` | Archivos adjuntos | - |
| `FOTO CEDULA VERDE` | Archivos adjuntos | - |
| `FOTO CARNET CONDUCIR` | Archivos adjuntos | - |
| `FOTO DAÑO DEL VEHICULO` | Archivos adjuntos | - |
| `FOTO DE DENUNCIA OFICIAL` | Archivos adjuntos | - |
| `FOTO  ACTA DE BOMBERO ( EN CASO DE iNCENDIO )` | Archivos adjuntos | - |
| `RAZON SOCIAL DEL TALLER` | Texto (multilínea) | - |
| `DOMICILIO` | Texto (línea única) | - |
| `TELEFONO 2` | Teléfono | - |
| `ESTADO DE LA POLIZA` | Selección única | Opciones: VIGENTE, ANULADA |
| `ESTADO DEL RECLAMO` | Selección única | Opciones: RESUELVE CON ABOGADO PERSONAL, RESUELVE CON ABOGADO NUESTRO, RESUELVE CON TALLER... |
| `TRATAMIENTO` | Selección única | Opciones: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO-A LA ESPERA DE RESPUESTA... |
| `OBSERVACIONES` | Texto (multilínea) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `TIPO DE CONSULTA` | Selección múltiple | Opciones: ROBO , INCENDIO |
| `DEJA CON FRECUENCIA VEHÍCULO AQUÍ` | Selección única | Opciones: SÍ, NO |
| `TENÍA ALARMA ACTIVADA` | Selección única | Opciones: SÍ, NO |
| `TIPO DE LUGAR` | Selección única | Opciones: PÚBLICO, PRIVADO |
| `TIENE CÁMARA DE SEGURIDAD` | Selección única | Opciones: SÍ, NO |
| `HUBO TESTIGOS` | Selección única | Opciones: SI, NO |
| `N° POLIZA` | Vínculo a registros | → POLIZAS |
| `N° DE POLIZA (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `PRODUCTO LINK` | Vínculo a registros | → PRODUCTOS |
| `TIPO DE PRODUCTOS (Rollup)` | Rollup (agregación) | Rollup: N/A |
| `FRECUENCIA DEL VEHÍCULO` | Selección única | Opciones: DIARIA, SEMANAL, MENSUAL... |
| `ESTADO_WEB` | Selección única | Opciones: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `NUMERO` | Desconocido (autoNumber) | - |
| `datos adjunto portal cliente` | Archivos adjuntos | - |
| `ID_REGISTRO_CLIENTE_LOOKUP` | Desconocido (multipleLookupValues) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |

### 🔗 Relaciones con Otras Tablas

- **ATENDIDO X** → `EMPLEADOS`
- **OFICINAS** → `OFICINAS`
- **CARGADO EN CIA X** → `EMPLEADOS`
- **CLIENTE** → `CLIENTES`
- **CÓDIGO EMISÍON DE PÓLIZA** → `OFICINAS`
- **N° POLIZA** → `POLIZAS`
- **PRODUCTO LINK** → `PRODUCTOS`
- **POLIZAS** → `POLIZAS`

---

## 🗂️ PRIMA CALCULADA

**ID:** `tblWc8dok3xKCAQSv`  
**Total de Campos:** 13  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `NUMERO DE POLIZA` | Desconocido (autoNumber) | - |
| `NOMBRE DEL CLIENTE` | Texto (línea única) | - |
| `PRIMA SUGERIDA` | Desconocido (richText) | - |
| `RECOMENDACION DE POLIZA` | Desconocido (richText) | - |
| `JUSTIFICACION` | Desconocido (richText) | - |
| `STATUS` | Selección única | Opciones: EN REVISION, ENVIADO, ACEPTADO... |
| `CLIENTE (relación)` | Vínculo a registros | → CLIENTES |
| `DNI (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `EMAIL (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `ID UNICO CLIENTE (de CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |

### 🔗 Relaciones con Otras Tablas

- **CLIENTE (relación)** → `CLIENTES`

---

## 🗂️ Nueva Tabla

**ID:** `tblbdS9dRFe0LttWr`  
**Total de Campos:** 11  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `CODIGO DE POLIZA` | Texto (línea única) | - |
| `NOMBRE Y APELLIDO` | Texto (línea única) | - |
| `CORREO ELECTRONICO` | Email | - |
| `FOTO DEL SINIESTRO` | Archivos adjuntos | - |
| `CLIENTE` | Texto (línea única) | - |
| `DNI (CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `TELEFONO (CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `EMAIL (CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `ID UNICO CLIENTE (CLIENTE)` | Desconocido (multipleLookupValues) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |

---

## 🗂️ TRAZABILIDAD/IA

**ID:** `tbll7KpmHHRUNcNqL`  
**Total de Campos:** 14  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID/TRAZABILIDAD` | Fórmula | Fórmula: `IF(
  {fldHEWhD4YpgGjtuo},
  {fldHEWhD4YpgGjtuo} &...` |
| `Última modificación` | Fecha de modificación | - |
| `Fecha y Hora de Creación (Automática)` | Fecha de creación | - |
| `ID_UNICO_CLIENTE` | Texto (línea única) | - |
| `ID_GESTION_UNICO` | Texto (línea única) | - |
| `Tipo de interacción` | Selección única | Opciones: Nueva denuncia, Consulta estado, Documentación... |
| `Interacción Resultado` | Selección única | Opciones: Formulario enviado, En proceso, Pendiente... |
| `Notas` | Texto (multilínea) | - |
| `Agente Responsable` | Selección única | Opciones: Manual, Agente Virtual BledSRL |
| `Canal de Contacto` | Selección única | Opciones: Teléfono, Email, WhatsApp... |
| `Adjuntos de Interacción` | Archivos adjuntos | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `ID_TRAZABILIDAD` | Desconocido (autoNumber) | - |

---

## 🗂️ CARGA DE DOCUMENTOS

**ID:** `tblmX2IuVPbe3rEf0`  
**Total de Campos:** 9  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID_GESTION_UNICO` | Texto (línea única) | - |
| `ESTADO` | Selección única | Opciones: Pendiente, Procesado |
| `FOTO DNI` | Archivos adjuntos | - |
| `FOTO CEDULA VERDE` | Archivos adjuntos | - |
| `FOTO CARNET CONDUCIR` | Archivos adjuntos | - |
| `FOTO DE DENUNCIA OFICIAL` | Archivos adjuntos | - |
| `FOTO DAÑO DEL VEHICULO` | Archivos adjuntos | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |

---

## 🗂️ COMPANIA

**ID:** `tbl8jENHY2lESAA5b`  
**Total de Campos:** 13  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `NOMBRE` | Texto (línea única) | - |
| `LOGO` | Archivos adjuntos | - |
| `TEL. AUXILIO` | Teléfono | - |
| `TEL. SINIESTROS` | Teléfono | - |
| `EMAIL SINIESTROS` | Email | - |
| `PORTAL PRODUCTORES` | URL | - |
| `CUIT` | Texto (línea única) | - |
| `EJECUTIVO DE CUENTA` | Texto (línea única) | - |
| `NOTAS INTERNAS` | Desconocido (richText) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `PRODUCTO LINK` | Vínculo a registros | → PRODUCTOS |
| `GESTIÓN GENERAL` | Vínculo a registros | → GESTIÓN GENERAL |
| `Recuento (POLIZAS)` | Conteo | - |

### 🔗 Relaciones con Otras Tablas

- **POLIZAS** → `POLIZAS`
- **PRODUCTO LINK** → `PRODUCTOS`
- **GESTIÓN GENERAL** → `GESTIÓN GENERAL`

---

## 🗂️ PRODUCTOS

**ID:** `tblB06Eo9ep7PhCU6`  
**Total de Campos:** 10  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `NOMBRE PRODUCTO` | Texto (línea única) | - |
| `ICONO` | Texto (línea única) | - |
| `DESCRIPCION` | Desconocido (richText) | - |
| `COMPANIA` | Vínculo a registros | → COMPANIA |
| `COBERTURAS DISPONIBLES` | Desconocido (richText) | - |
| `POLIZAS` | Vínculo a registros | → POLIZAS |
| `Recuento (POLIZAS)` | Conteo | - |
| `DENUNCIA ROBO / INCENDIO` | Vínculo a registros | → DENUNCIA ROBO / INCENDIO |
| `GESTIÓN GENERAL 2` | Vínculo a registros | → GESTIÓN GENERAL |
| `DENUNCIA ROBO OC` | Texto (línea única) | - |

### 🔗 Relaciones con Otras Tablas

- **COMPANIA** → `COMPANIA`
- **POLIZAS** → `POLIZAS`
- **DENUNCIA ROBO / INCENDIO** → `DENUNCIA ROBO / INCENDIO`
- **GESTIÓN GENERAL 2** → `GESTIÓN GENERAL`

---

## 🗂️ LOGIN

**ID:** `tblncx3WdvTfJRVck`  
**Total de Campos:** 12  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `EMAIL` | Email | - |
| `CONTRASEÑA` | Texto (línea única) | - |
| `ROL` | Selección única | Opciones: Empleado, Gerente, Dueño... |
| `ROL OPERATIVO` | Fórmula | Fórmula: `TRIM({fld1P86jVMhICO9eA} & "")` |
| `ESTADO` | Selección única | Opciones: Activo, Inactivo, Pendiente |
| `URL_PORTAL` | Fórmula | Fórmula: `IF(
  {fldMt4uWj6v1mJcCK} = "Activo",
  SWITCH(
  ...` |
| `EMPLEADO` | Vínculo a registros | → EMPLEADOS |
| `NOMBRE Y APELLIDO` | Fórmula | Fórmula: `UPPER(CONCATENATE({fldBIZajRtb17tb8f}, " ", {fldJW...` |
| `NOMBRE` | Texto (línea única) | - |
| `APELLIDO` | Texto (línea única) | - |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIIFICACION` | Fecha de modificación | - |

### 🔗 Relaciones con Otras Tablas

- **EMPLEADO** → `EMPLEADOS`

---

## 🗂️ PORTAL

**ID:** `tblPMS1P9bKdtCJLL`  
**Total de Campos:** 4  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID` | Desconocido (autoNumber) | - |
| `ROL` | Selección múltiple | Opciones: EMPLEADO, GERENTE, DUEÑO |
| `FRASES DEL PORTAL` | Desconocido (aiText) | - |
| `FOTOS DEL PORTAL` | Archivos adjuntos | - |

---

## 🗂️ Tokens

**ID:** `tblli6UbYYejemlhQ`  
**Total de Campos:** 5  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `TOKEN` | Texto (línea única) | - |
| `URL_DESTINO` | URL | - |
| `EXPIRA` | Texto (línea única) | - |
| `USADO` | Checkbox (Sí/No) | - |
| `EMAIL_USUARIO` | Texto (línea única) | - |

---

## 🗂️ CALIFICACIONES

**ID:** `tblMzfmEfLNNzaJqZ`  
**Total de Campos:** 17  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ESTRELLAS` | Número | - |
| `NOMBRE` | Texto (línea única) | - |
| `ES_CLIENTE` | Selección única | Opciones: Sí, No |
| `DNI` | Número | - |
| `SERVICIO` | Selección única | Opciones: Atención General, Cotización, Siniestro... |
| `COMENTARIO` | Texto (multilínea) | - |
| `MODO` | Selección única | Opciones: Online, Presencial |
| `VISIBLE` | Checkbox (Sí/No) | - |
| `EMPLEADO` | Vínculo a registros | → EMPLEADOS |
| `CLIENTE` | Vínculo a registros | → CLIENTES |
| `FOTO PERFIL` | Desconocido (multipleLookupValues) | - |
| `CUAL FUE TU EXPERIENCIA CON NOSOTROS` | Calificación | - |
| `URGENCIA DE ATENCION (AI)` | Selección única | Opciones: Atender urgente, Próximo a contactar, Calificación cerrada |
| `FECHA DE CREACION` | Fecha de creación | - |
| `ULTIMA MODIFICACION` | Fecha de modificación | - |
| `AUTORIZA_PUBLICAR` | Checkbox (Sí/No) | - |
| `USAR FOTO` | Checkbox (Sí/No) | - |

### 🔗 Relaciones con Otras Tablas

- **EMPLEADO** → `EMPLEADOS`
- **CLIENTE** → `CLIENTES`

---

## 🗂️ BIBLIOTECA_AUDIOS

**ID:** `tblUKC1y9HcCcYx0A`  
**Total de Campos:** 10  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `CODIGO_ID` | Texto (línea única) | - |
| `ARCHIVO_AUDIO` | Archivos adjuntos | - |
| `ASUNTO_EMAIL` | Texto (línea única) | - |
| `CUERPO_EMAIL` | Desconocido (richText) | - |
| `DESCRIPCION_INTERNA` | Texto (línea única) | - |
| `URL_PUBLICA` | Fórmula | Fórmula: `IF(
  {fldTv7GKGytE8sRQd},
  {fldTv7GKGytE8sRQd}
)` |
| `CREADO_POR` | Creado por | - |
| `FECHA_CREACION` | Fecha de creación | - |
| `FECHA_ULTIMA_MODIFICACION` | Fecha de modificación | - |
| `VISIBLE_A_CLIENTES` | Checkbox (Sí/No) | - |

---

## 🗂️ CONFIG_FORMULARIOS

**ID:** `tblbkMQlI9BpGQndA`  
**Total de Campos:** 7  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `CODIGO` | Texto (línea única) | - |
| `TITULO` | Texto (línea única) | - |
| `ICONO` | Texto (línea única) | - |
| `COLOR` | Texto (línea única) | - |
| `CONFIG_CAMPOS` | Vínculo a registros | → CONFIG_CAMPOS |
| `TABLA RELACIONADA` | Texto (línea única) | - |
| `VISIBILIDAD` | Checkbox (Sí/No) | - |

### 🔗 Relaciones con Otras Tablas

- **CONFIG_CAMPOS** → `CONFIG_CAMPOS`

---

## 🗂️ CONFIG_CAMPOS

**ID:** `tblBJoFWFZxHo8zpq`  
**Total de Campos:** 8  

### 📋 Campos

| Campo | Tipo | Detalles |
|-------|------|----------|
| `ID CAMPO` | Texto (línea única) | - |
| `ETIQUETA` | Texto (línea única) | - |
| `TIPO` | Selección única | Opciones: Single line text (Texto de una línea), Long text (Texto largo), Rich text (Texto con formato)... |
| `OPCIONES` | Texto (multilínea) | - |
| `OBLIGATORIO` | Checkbox (Sí/No) | - |
| `ORDEN` | Número | - |
| `FORMULARIO` | Vínculo a registros | → CONFIG_FORMULARIOS |
| `COLUMNA AIRTABLE` | Texto (línea única) | - |

### 🔗 Relaciones con Otras Tablas

- **FORMULARIO** → `CONFIG_FORMULARIOS`

---


## 🐍 Uso en Backend Python

### Tablas Usadas en Backend:

- **CLIENTES**: 4 referencias
- **POLIZAS**: 5 referencias
- **CALIFICACIONES**: 3 referencias
- **CONFIG_FORMULARIOS**: 2 referencias
- **CONFIG_CAMPOS**: 2 referencias


## 🌐 Conexión con Frontend

### Endpoints del Frontend:

| Endpoint | Descripción |
|----------|-------------|
| `/api/validate-siniestro` | Valida cliente y póliza (CLIENTES, POLIZAS) |
| `/api/config-formularios` | Lee CONFIG_FORMULARIOS y CONFIG_CAMPOS |
| `/api/create-siniestro` | Crea registro en tabla dinámica de siniestros |
| `/api/rating` | Lee/escribe en tabla de calificaciones |
| `/api/testimonios` | Lee testimonios públicos |


## 💡 Recomendaciones y Hallazgos

### ✅ Campos Correctamente Configurados
- Campos de relación entre CLIENTES, POLIZAS y tablas de siniestros
- Sistema de CONFIG_FORMULARIOS y CONFIG_CAMPOS dinámico

### ⚠️ Posibles Mejoras
- Verificar que todos los campos usados en backend existan en las tablas
- Asegurar que las fórmulas de ID_GESTION_UNICO estén configuradas
- Revisar campos de tipo "lookup" y "rollup" para optimización

### 🔍 Próximos Pasos
1. Comparar este reporte con FULL_DB_SCHEMA.md desactualizado
2. Actualizar documentación oficial
3. Validar que no haya campos hardcodeados en código que no existan en Airtable
