# 🛡️ FULL DB SCHEMA - SISTEMA GESTION DE SEGUROS AGENTICO

Este documento es la **ÚNICA FUENTE DE VERDAD** sobre la estructura de Airtable.

## 📄 CLIENTES
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `NOMBRE NORMALIZADO` | formula | `SUBSTITUTE(
  SUBSTITUTE(
    SUBSTITUTE(
      SUBSTITUTE(
        SUBSTITUTE(
          UPPER({fldMOWE14jxebYFBG} & " " & {fldZhc0hVbwL4BwuE}),
          "Á", "A"
        ),
        "É", "E"
      ),
      "Í", "I"
    ),
    "Ó", "O"
  ),
  "Ú", "U"
)` |
| `🏷️ ESTADO_CLIENTE` | formula | `REGEX_REPLACE(
  TRIM(
    IF(
      {fldT7EQqTHHXQvYUS} != '',
        '🔴 CLIENTE BAJA',
        TRIM(
          IF({fldFOWGHtgmFHaO7r} > 0,
            '🟢 ' & {fldFOWGHtgmFHaO7r} & ' ' & IF({fldFOWGHtgmFHaO7r} = 1, 'ACTIVA', 'ACTIVAS'),
            ''
          ) &
          IF(AND({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0), '\n', '') &
          IF({flduTAlxnGjnWqXvy} > 0,
            '🔴 ' & {flduTAlxnGjnWqXvy} & ' ' & IF({flduTAlxnGjnWqXvy} = 1, 'ANULADA', 'ANULADAS'),
            ''
          ) &
          IF(OR({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0), IF({fldff48Z4DaPo9rHe} > 0, '\n', ''), '') &
          IF({fldff48Z4DaPo9rHe} > 0,
            '🟡 ' & {fldff48Z4DaPo9rHe} & ' EN TRÁMITE',
            ''
          ) &
          IF(OR({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0, {fldff48Z4DaPo9rHe} > 0), IF({fldOqKQoYh4DjK9fi} > 0, '\n', ''), '') &
          IF({fldOqKQoYh4DjK9fi} > 0,
            '🟠 ' & {fldOqKQoYh4DjK9fi} & ' SIN VIGENCIA',
            ''
          ) &
          IF(OR({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0, {fldff48Z4DaPo9rHe} > 0, {fldOqKQoYh4DjK9fi} > 0), IF({fldkedqaL1ZSTJTWb} > 0, '\n', ''), '') &
          IF({fldkedqaL1ZSTJTWb} > 0,
            '⭕ ' & {fldkedqaL1ZSTJTWb} & ' SIN PÓLIZA',
            ''
          ) &
          IF(OR({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0, {fldff48Z4DaPo9rHe} > 0, {fldOqKQoYh4DjK9fi} > 0, {fldkedqaL1ZSTJTWb} > 0), IF({fldPYrKHjdYoDKmeg} > 0, '\n', ''), '') &
          IF({fldPYrKHjdYoDKmeg} > 0,
            '⏰ ' & {fldPYrKHjdYoDKmeg} & ' VENCE EN 7 DÍAS',
            ''
          ) &
          IF(OR({fldFOWGHtgmFHaO7r} > 0, {flduTAlxnGjnWqXvy} > 0, {fldff48Z4DaPo9rHe} > 0, {fldOqKQoYh4DjK9fi} > 0, {fldkedqaL1ZSTJTWb} > 0, {fldPYrKHjdYoDKmeg} > 0), IF({fld9Qf9yuHTo7R6Ir} > 0, '\n', ''), '') &
          IF({fld9Qf9yuHTo7R6Ir} > 0,
            '⏳ ' & {fld9Qf9yuHTo7R6Ir} & ' VENCE EN 30 DÍAS',
            ''
          )
        )
    )
  ),
  "[ ]+",
  " "
)` |
| `✅ CANTIDAD_POLIZAS` | rollup |  |
| `🟢 POLIZAS_ACTIVAS` | rollup |  |
| `🔴 POLIZAS_ANULADAS` | rollup |  |
| `🟡 POLIZAS_EN_TRAMITES` | rollup |  |
| `🟣 POLIZAS_SIN_VIGENCIA` | rollup |  |
| `⭕ SIN_POLIZAS` | rollup |  |
| `📆 LA_POLIZAS VENCE EN 30 DIAS` | rollup |  |
| `📆 LA_POLIZAS VENCE EN 7 DIAS` | rollup |  |
| `APELLIDO` | singleLineText |  |
| `NOMBRES` | singleLineText |  |
| `ID_UNICO_CLIENTE` | formula | `"🆔 " & RIGHT(CONCATENATE({fldgfcpYGlVrRACcb}), 3) & UPPER(LEFT({fldzJskztOW1uotuc}, 3))` |
| `DNI` | number |  |
| `TELEFONO` | phoneNumber |  |
| `EMAIL` | email |  |
| `DIRECCION` | richText |  |
| `FOTO PERFIL` | multipleAttachments |  |
| `CREADO X` | singleSelect | Options: AGENTE IA, ASESOR |
| `EMPLEADOS` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `NOTAS` | richText |  |
| `FECHA DE ALTA` | createdTime |  |
| `FECHA DE BAJA` | date |  |
| `DENUNCIA DE ACCIDENTE` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `PRIMA CALCULADA` | multipleRecordLinks | Link to `tblWc8dok3xKCAQSv` |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 6` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `OFICINAS` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `OFICINAS Compilación (de GESTIÓN GENERAL)` | rollup |  |
| `OFICINAS Compilación (de CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))` | rollup |  |
| `GESTIÓN GENERAL` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `MOTIVOS DE LA CONSULTA Compilación (de GESTIÓN GENERAL)` | multipleLookupValues |  |
| `TIPO DE PRODUCTOS (de GESTIÓN GENERAL)` | multipleLookupValues |  |
| `COBERTURA (de GESTIÓN GENERAL)` | multipleLookupValues |  |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL)` | multipleLookupValues |  |
| `N° DE POLIZA (de GESTIÓN GENERAL)` | multipleLookupValues |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `ETIQUETA_POLIZA Compilación (de POLIZAS)` | rollup |  |
| `ID_REGISTRO_CLIENTE` | formula | `RECORD_ID()` |
| `IR A CLIENTE` | button |  |
| `CALIFICACIONES` | multipleRecordLinks | Link to `tblMzfmEfLNNzaJqZ` |
| `CONTRASEÑA PORTAL` | singleLineText |  |

---

## 📄 EMPLEADOS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `NOMBRE Y APELLIDO` | singleLineText |  |
| `NOMBRE Y APELLIDO NORMALIZADO` | formula | `UPPER({fldnLBeF1MB6KUdO4})` |
| `ID_UNICO_EMPLEADO` | formula | `CONCATENATE(
  LEFT({fldnLBeF1MB6KUdO4}, 3),
  IF(
    FIND("-", {fldUgeAhm9XzbsdLT}) > 0,
    RIGHT(
      MID(
        {fldUgeAhm9XzbsdLT},
        FIND("-", {fldUgeAhm9XzbsdLT}) + 1,
        FIND("-", {fldUgeAhm9XzbsdLT}, FIND("-", {fldUgeAhm9XzbsdLT}) + 1) - FIND("-", {fldUgeAhm9XzbsdLT}) - 1
      ),
      3
    ),
    RIGHT({fldUgeAhm9XzbsdLT}, 3)
  )
)` |
| `CUIL` | singleLineText |  |
| `DOMICILIO` | singleLineText |  |
| `LOCALIDAD` | singleLineText |  |
| `TELEFONO` | phoneNumber |  |
| `EMAIL` | email |  |
| `FECHA NAC.` | date |  |
| `CUENTA` | singleLineText |  |
| `INGRESO` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `BAJA` | date |  |
| `FOTO DE PERFIL` | multipleAttachments |  |
| `Recuento (GESTION GENERAL)` | count |  |
| `💰✅ TOTAL COMISIÓN FINAL Compilación (de GESTION GENERAL)` | rollup |  |
| `Recuento (GESTION GENERAL) DEL AÑO` | count |  |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) DEL AÑO` | rollup |  |
| `Recuento (GESTION GENERAL)  MES EN CUSRSO` | count |  |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) MES EN CURSO` | rollup |  |
| `Recuento (GESTION GENERAL)  DE LA SEMANA` | count |  |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) SEMANA EN CURSO` | rollup |  |
| `Recuento (GESTION GENERAL)  ES HOY` | count |  |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL) ES HOY` | rollup |  |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))TOTALES` | count |  |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))DEL AÑO` | count |  |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))MES CALENDARIO` | count |  |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))SEMANA CALENDARIO` | count |  |
| `Recuento (CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ))ES HOY` | count |  |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ))TOTALES` | count |  |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DEL AÑO` | count |  |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DEL MES` | count |  |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DE LA SEMANA` | count |  |
| `Recuento (CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )) DE HOY` | count |  |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)` | count |  |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)HOY` | count |  |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)SEMANA` | count |  |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)MES` | count |  |
| `Recuento (DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL)AÑO` | count |  |
| `FECHA DE CREACION` | createdTime |  |
| `COMISIONES` | singleLineText |  |
| `DENUNCIA DE ACCIDENTE` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `DENUNCIA ROBO OC` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `Resumen Total Anual` | formula | `"TOTAL DE GESTION GENERAL ANUAL: " & {fldyRnnow5QcV4Ca8} & "\n" &
"TOTAL DE ACCIDENTE ANUAL: " & {fldN9P1Yn2nwoNbhR} & "\n" &
"TOTAL DE ROBO INCENDIO ANUAL: " & {fldHd94xIHbCvO4HO} & "\n" &
"TOTAL DE ROBO OC ANUAL: " & {fld3A5q0DjI7CEJxe} & "\n" &
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" &
"TOTAL GENERAL ANUAL: " & (
  {fldyRnnow5QcV4Ca8} +
  {fldN9P1Yn2nwoNbhR} +
  {fldHd94xIHbCvO4HO} +
  {fld3A5q0DjI7CEJxe}
)` |
| `COMISIONES MEJORADAS` | singleLineText |  |
| `Login` | multipleRecordLinks | Link to `tblncx3WdvTfJRVck` |
| `CONTRASEÑA (from Login)` | multipleLookupValues |  |
| `ROL OPERATIVO` | multipleLookupValues |  |
| `ESTADO DEL LOGIN` | multipleLookupValues |  |
| `GESTION GENERAL` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `💰✅ TOTAL COMISIÓN FINAL (de GESTION GENERAL)` | multipleLookupValues |  |
| `🟠 ALERTA PAGO EN EFECTIVO (de GESTION GENERAL)` | multipleLookupValues |  |
| `🔴 Aviso Comisión Cero (de GESTION GENERAL)` | multipleLookupValues |  |
| `FECHA (de GESTION GENERAL)` | multipleLookupValues |  |
| `CLIENTES` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `CALIFICACIONES` | multipleRecordLinks | Link to `tblMzfmEfLNNzaJqZ` |

---

## 📄 OFICINAS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `OFICINAS` | singleLineText |  |
| `NOMBRE_OFICINA_LIMPIO_WEB` | formula | `TRIM(REGEX_REPLACE({fldbRydM9VwwRAkVD}, " ?\\([^\\)]*\\)", ""))` |
| `LOCALIDAD DE OFICINAS` | singleLineText |  |
| `DOMICILIO` | singleLineText |  |
| `TELEFONO` | phoneNumber |  |
| `E-MAIL` | email |  |
| `HORARIO` | singleLineText |  |
| `GOOGLE MAP` | button |  |
| `GEOLOCALIZACION` | url |  |
| `FOTO` | multipleAttachments |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  TOTAL` | count |  |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  ANUAL` | count |  |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  SEMANAL` | count |  |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE  MENSUAL` | count |  |
| `CANTIDAD DE  DENUNCIA DE ACCIDENTE HOY` | count |  |
| `CANTIDAD DE GESTIONES GENERALES TOTAL` | count |  |
| `CANTIDAD DE GESTIONES GENERALES ANUAL` | count |  |
| `CANTIDAD DE GESTIONES GENERALES MENSUAL` | count |  |
| `CANTIDAD DE GESTIONES GENERALES SEMANAL` | count |  |
| `CANTIDAD DE GESTIONES GENERALES HOY` | count |  |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL  TOTAL` | count |  |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL  ANUAL` | count |  |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL MENSUAL` | count |  |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL SEMANAL` | count |  |
| `CANTIDAD DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL HOY` | count |  |
| `CANTIDAD CARGA DENUNCIA ROBO OC TOTAL` | count |  |
| `CANTIDAD CARGA DENUNCIA ROBO OC ANUAL` | count |  |
| `CANTIDAD CARGA DENUNCIA ROBO OC MENSUAL` | count |  |
| `CANTIDAD CARGA DENUNCIA ROBO OC SEMANAL` | count |  |
| `CANTIDAD CARGA DENUNCIA ROBO OC  HOY` | count |  |
| `Resumen Cantidades y Total General` | formula | `"TOTAL DE GESTION GENERAL: " & {fldgtOOZUgcMNz54c} & "\n" &
"TOTAL DE ACCIDENTE: " & {fldYnnUeJobL2D9G6} & "\n" &
"TOTAL DE ROBO INCENDIO: " & {flduTUCAb2W3PSlig} & "\n" &
"TOTAL DE ROBO OC: " & {flde0gTUBSbzU34gm} & "\n" &
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" &
"TOTAL GENERAL: " & (
  {fldgtOOZUgcMNz54c} +
  {fldYnnUeJobL2D9G6} +
  {flduTUCAb2W3PSlig} +
  {flde0gTUBSbzU34gm}
)` |
| `ORDEN` | number |  |
| `VISIBILIDAD` | checkbox |  |
| `CARGA DE DENUNCIA DE ACCIDENTE  MENSUAL` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `GESTIÓN GENERAL 2` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 3` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 4` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `CLIENTES` | singleLineText |  |
| `CLIENTES 2` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |

---

## 📄 GESTIÓN GENERAL
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_UNICO_GESTION` | formula | `CONCATENATE({fld0wPLry103yD2Il}, "/", {fldkcOLXVUX7NYc9b}, "GG🔵")` |
| `CLIENTE` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DNI (from CLIENTE)` | multipleLookupValues |  |
| `TELEFONO (from CLIENTE)` | multipleLookupValues |  |
| `EMAIL (from CLIENTE)` | multipleLookupValues |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `OFICINAS` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `ES CLIENTE` | singleSelect | Options: No, Si |
| `MOTIVOS DE LA CONSULTA` | singleSelect | Options: COTIZACIÓN, ALTAS, ANULACIÓN, COBRANZA, NO APLICA, ENDOSO, IMPRESIÓN / RETIRO DOCU, OTROS , SINIESTRO, POLIZA ACTIVADA |
| `TIPO DE PRODUCTOS` | multipleRecordLinks | Link to `tblB06Eo9ep7PhCU6` |
| `TIPO ENDOSO / ANULACIÓN` | singleSelect | Options: NO APLICA, ANULA POR MOTIVOS VS, DESESTIMA ASEGURADO, ANULA POR VENTA, CAMBIO FORMA DE PAGO, ADICIONA GNC/CRIS/CERRAD, ANULA SINIESTRO, ANULA CAMBIO DE COMPANIA, ANULA POR ERROR DE EMISIÓN, ANULA POR MOTIVOS VARIOS, ANULA POR MOTIVOS DE COSTOS, AUMENTO DE COBERTURA, BONIFICACIÓN, CAMBIO EN NOMINA, CAMBIO DE UNIDAD, DISMINUCIÓN DE COBERTURA, MODIFICA SUMA ASEGURADA, CAMBIO DATOS TOMAD0R, CAMBIO DATOS DEL VEHÍCULO |
| `COBERTURA` | singleSelect | Options: A, B, B1, B4, C, C1, C2, C2FULL, D3, COBERTURA, NO APLICA, TR |
| `FORMA DE PAGOS` | singleSelect | Options: CREDITO, DEBITO, EFECTIVO, NO APLICA |
| `IMPORTE` | currency |  |
| `VIDA` | singleSelect | Options: N CREDITO, No, Si |
| `IMPORTE VIDA` | currency |  |
| `AUXILIOS` | singleSelect | Options: AUX 100, AUX 300, AUX 500, AUX INFINITY, AUX URBANO 20, AUX AVENTURA 100, NO, AUX |
| `IMPORTE AUX 24` | currency |  |
| `ATENDIDO X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `Escribe tu ID` | singleLineText |  |
| `TIPO DE ATENCIÓN` | singleSelect | Options: AUTO-GESTIÓN, PRESENCIAL, WLVX, WAPP - PERSONAL, VÍA E-MAIL, WAPP-PERSONAL, 0810-AUTO-GESTIÓN, AGENTE IA |
| `RECUPERO` | singleSelect | Options: NO, SI |
| `RENOVACIÓN` | singleSelect | Options: NO, SI |
| `DETALLAR OTROS` | richText |  |
| `COMISIÓN VIDA` | formula | `{fldm4h2HWbR0KUuiz}` |
| `💰 TOTAL COMISIÓN` | formula | `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b8cNvoIKGwsbt}` |
| `💰✅ TOTAL COMISIÓN FINAL` | formula | `IF({fldTukq50AVcZM8Eu} = 'N CREDITO', {fldFTtvSdMa6eSNN7} + {fldm4h2HWbR0KUuiz}, {fldFTtvSdMa6eSNN7})` |
| `🟠 ALERTA PAGO EN EFECTIVO` | formula | `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', '🟠 Alerta: Pago en Efectivo', '')` |
| `🔴 Aviso Comisión Cero` | formula | `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8EbNtYgrelv} = 0, DATETIME_DIFF(TODAY(), {fldsitgCySZods6Il}, 'days') >= 30), '🔴 Comisión es 0', '')` |
| `TIPO DE SOLICITUD` | singleSelect | Options: COTIZACIÓN, ALTA PRODUCTO, DENUNCIA ACCIDENTE, DENUNCIA ROBO / INCENDIO, DENUNCIA ROBO OC, CONSULTA, GESTIÓN ADMINISTRATIVA |
| `ESTADO DE LA SOLICITUD` | singleSelect | Options: NUEVA, EN PROCESO, FINALIZADA, REQUIERE DOCUMENTACIÓN, RECHAZADA, PENDIENTE DE VALIDACIÓN |
| `FECHA DE SOLICITUD` | date |  |
| `COMENTARIOS DEL CLIENTE` | multilineText |  |
| `NOTIFICACIONES PORTAL CLIENTE` | multipleSelects | Options: NUEVA SOLICITUD, SOLICITUD EN PROCESO, SOLICITUD FINALIZADA, SE REQUIEREN DOCUMENTOS, CAMBIO EN LA GESTIÓN, COTIZACIÓN DISPONIBLE, ALTA EXITOSA, SOLICITUD RECHAZADA |
| `DOCUMENTOS SOLICITADOS` | multipleAttachments |  |
| `datos adjunto portal cliente` | multipleAttachments |  |
| `ID_REGISTRO_CLIENTE_LOOKUP` | multipleLookupValues |  |
| `IR A CLIENTE` | button |  |
| `COMISIONES MEJORADAS` | singleLineText |  |
| `NUMERO` | autoNumber |  |
| `FOTO PERFIL (de CLIENTE)` | multipleLookupValues |  |
| `ID_UNICO_CLIENTE` | multipleLookupValues |  |
| `🔢✅ Cantidad de ALTAS` | formula | `IF({fldQSvgctDcTZ9TXY} = 'ALTAS', 1, 0)` |
| `🔢 ❌ Cantidad de ANULACIÓN` | formula | `IF({fldQSvgctDcTZ9TXY} = 'ANULACIÓN', 1, 0)` |
| `🔢 ✳️Diferencia ALTAS-ANULACIÓN` | formula | `{fldSspNQJl5SPV40x} - {fld5oogxxETzlGnRg}` |
| `JAJAJA` | formula | `IF(OR({fldi0omqIDbHpxO1O} > 0, {fld2b8cNvoIKGwsbt} > 0), {fldtCYI9REtFaInLB} * 0.08, IF(AND({fldi0omqIDbHpxO1O} = 0, {fld2b8cNvoIKGwsbt} = 0), {fldtCYI9REtFaInLB} * 0.02, 0))` |
| `💼 COMISIÓN VIDA + JAJAJA` | formula | `{fldi0omqIDbHpxO1O} + {fldn734Iq6YJKVMV0}` |
| `COMISIÓN AUX` | formula | `{fldtcTWSS2ffbzuZ7} / 2` |
| `COMISIÓN AUX + JAJAJA` | formula | `{fld2b8cNvoIKGwsbt} + {fldn734Iq6YJKVMV0}` |
| `💵 COMISIÓN ALTA SIMPLE` | formula | `{fldtCYI9REtFaInLB} * 0.02` |
| `💲 TOTAL COMI COMBINADAS` | formula | `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b8cNvoIKGwsbt}` |
| `✅💰 TOTAL COMISIÓN FINAL 1` | formula | `IF({fldQSvgctDcTZ9TXY} != 'ALTAS', 0, {fldanV8EbNtYgrelv})` |
| `💰 TOTAL COMISIÓN AJUSTADA` | formula | `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', 0, {fldmhPEfrraHkRiuU})` |
| `Copia de 🔴 Aviso Comisión Cero` | formula | `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8EbNtYgrelv} = 0, DATETIME_DIFF(NOW(), {fldsitgCySZods6Il}, 'minutes') >= 5), '🔴 Comisión es 0', '')` |
| `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )` | singleLineText |  |
| `CLIENTES` | singleLineText |  |
| `PATENTE DEL VEHICULO` | singleLineText |  |
| `DENUNCIA DE ACCIDENTE` | singleLineText |  |
| `DENUNCIA DE ACCIDENTE 2` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `MARCA` | singleLineText |  |
| `MODELO` | singleLineText |  |
| `AÑO DEL VEHICULO` | number |  |
| `N° DE POLIZA` | multipleLookupValues |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `N°  POLIZA GESTIONADA` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `COMPANIA` | multipleRecordLinks | Link to `tbl8jENHY2lESAA5b` |

---

## 📄 POLIZAS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_UNICO_GESTION` | singleLineText |  |
| `FECHA VENCIMIENTO DE LA POLIZA` | date |  |
| `ACTIVAR POLIZA` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `ESTADO DE LA POLIZA` | singleSelect | Options: ALTA , ANULACION, EN TRAMITE, SIN POLIZA, SIN VIGENCIA, VENCE EN 30 DIAS, VENCE EN 7 DIAS |
| `N° DE POLIZA` | singleLineText |  |
| `CLIENTES` | singleLineText |  |
| `ARTICULO` | singleLineText |  |
| `N° CERTIFICADO` | singleLineText |  |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES)` | singleLineText |  |
| `COBERTURA` | singleSelect | Options: A, B, B4, C, C1, C2, C2FULL, D3, NO APLICA, TR |
| `MARCA DEL VEHICULO` | singleLineText |  |
| `MODELO DEL VEHICULO` | singleLineText |  |
| `AÑO DEL VEHICULO` | number |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `COMISIONES MEJORADAS` | singleLineText |  |
| `DENUNCIA ROBO / INCENDIO` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `GESTIÓN GENERAL` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `CLIENTES 2` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DENUNCIA DE ACCIDENTE` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `DENUNCIA DE ACCIDENTE 2` | multipleRecordLinks | Link to `tbl4570W1T0qGdj8w` |
| `TIPO DE COMBUSTIBLE` | singleSelect | Options: NAFTA, GASOIL, GNC, ELECTRICO, HIBRIDOS |
| `USO DEL VEHICULO` | singleLineText |  |
| `FECHA DE INICIO DE LA POLIZA` | date |  |
| `ETIQUETA_POLIZA` | formula | `UPPER(
  SWITCH(
    {fldkSsKEPwgEBkRQS},
    "ALTA ", " 🟢 ALTA",
    "ANULACION", " 🔴 ANULADA",
    "EN TRAMITE", " 🟡 EN TRÁMITE",
    "SIN VIGENCIA", " 🟣 SIN VIGENCIA",
    "SIN POLIZA", " ⭕ SIN PÓLIZA",
    "VENCE EN 30 DIAS", " ⏳ VENCE 30D",
    "VENCE EN 7 DIAS", " ⏰ VENCE 7D",
    "❓ " & {fldkSsKEPwgEBkRQS}
  )
) & "   |   " &
IF(
  FIND("MOTO", UPPER(ARRAYJOIN({fld01N12rxhT4hBVS}, ""))),
  "🛵",
  "🚗"
) & " " & ARRAYJOIN({fld01N12rxhT4hBVS}, ", ") &
"   |   " &
"N° POL: " & IF(
  {fldvh10rPHgmShMYA},
  {fldvh10rPHgmShMYA},
  IF({fldkSsKEPwgEBkRQS} = "EN TRAMITE", "PENDIENTE", "S/N")
) &
"   |   🏷️ " & ARRAYJOIN({fldBDRAUPMoMEfzH5}, ", ") &
"   |   🛡️ " & ARRAYJOIN({fldBXTEc3A5dJjcn3}, ", ") &
IF(
  AND(
    {fld3vyp2FvceuhgJ7},
    ARRAYJOIN({fld3vyp2FvceuhgJ7}, "") != "",
    UPPER(ARRAYJOIN({fld3vyp2FvceuhgJ7}, "")) != "NO"
  ),
  "   |   ❤️ VIDA: " & ARRAYJOIN({fld3vyp2FvceuhgJ7}, ", "),
  ""
) &
IF(
  AND(
    {fld2mseHidFS7QQmq},
    ARRAYJOIN({fld2mseHidFS7QQmq}, "") != "",
    UPPER(ARRAYJOIN({fld2mseHidFS7QQmq}, "")) != "NO"
  ),
  "   |   🆘 " & ARRAYJOIN({fld2mseHidFS7QQmq}, ", "),
  ""
)` |
| `VIDA` | singleSelect | Options: Si, No, N CREDITO |
| `AUXILIO` | singleSelect | Options: AUX, AUX 300, AUX 500, AUX INFINITY, AUX URBANO 20, AUX AVENTURA, NO |
| `COMPANIA LINK` | multipleRecordLinks | Link to `tbl8jENHY2lESAA5b` |
| `EMAIL SINIESTROS (from COMPANIA LINK)` | multipleLookupValues |  |
| `TEL. AUXILIO (from COMPANIA LINK)` | multipleLookupValues |  |
| `LOGO (from COMPANIA LINK)` | multipleLookupValues |  |
| `PRODUCTO LINK` | multipleRecordLinks | Link to `tblB06Eo9ep7PhCU6` |
| `OFICINA` | singleLineText |  |
| `COMISIONES` | singleLineText |  |
| `DENUNCIA ROBO OC` | singleLineText |  |
| `DENUNCIA ROBO OC 2` | singleLineText |  |
| `DENUNCIA ROBO OC 3` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `DENUNCIA ROBO OC 4` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `DENUNCIA ROBO OC 5` | multipleRecordLinks | Link to `tblRsZQhnNdJqnxf8` |
| `DENUNCIA ROBO / INCENDIO 2` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `DOCUMENTACION` | multipleAttachments |  |

---

## 📄 DENUNCIA DE ACCIDENTE
( SIRVE TAMBIEN PARA DT Y TR )

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_GESTION_UNICO` | formula | `CONCATENATE(
  ARRAYJOIN({fldLrTr9OUePj5eER}, ""),
  "/",
  {fldXtfy3gY4QD5jzI},
  "CDA🔴"
)` |
| `FECHA CARGA` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `ESCRIBE TÚ ID` | singleLineText |  |
| `ATENDIDO X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `OFICINAS` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `TIPO DE ATENCIÓN` | singleSelect | Options: WLVX, PRESENCIAL, WAPP-PERSONAL, 0810-AUTO-GESTIÓN, VÍA E-MAIL, AGENTE IA, AUTO GESTIÓN WEB |
| `MOTIVOS DE LA CONSULTA` | singleSelect | Options: SINIESTRO |
| `TIPO DE PRODUCTOS` | multipleLookupValues |  |
| `ID_UNICO_CLIENTE` | multipleLookupValues |  |
| `CLIENTE` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DNI (de CLIENTES)` | multipleLookupValues |  |
| `TELEFONO (de CLIENTES)` | multipleLookupValues |  |
| `EMAIL (de CLIENTES)` | multipleLookupValues |  |
| `MARCA DEL VEHICULO` | singleLineText |  |
| `MODELO DEL  VEHICULO` | singleLineText |  |
| `AÑO DEL VEHICULO` | singleSelect | Options: 1975, 1982, 1971, 2024, 2021, 2015, 2017, 2022, 2011, 2020, 2013, 2005, 2010, 2012, 2023, 2019, 1980, 2016, 2006, 2018, 2014, 2007, 1999, 2009, 2008, 2000, 1997, 1994, 2004, 1996, 1998, 2003, 1991, 1993, 2025, 1989, 1995, 2001, 1990 |
| `CARGADO EN CIA X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `N° DE POLIZA Compilación (de POLIZAS 2)` | rollup |  |
| `MARCA (from NUMERO DE POLIZA)` | rollup |  |
| `MODELO DEL VEHICULO Compilación (de POLIZAS 2)` | rollup |  |
| `AÑO DEL VEHICULO (from NUMERO DE POLIZA)` | rollup |  |
| `PATENTE DEL VEHICULO` | rollup |  |
| `COBERTURA` | rollup |  |
| `CODIGO EMISION DE LA POLIZA` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `ARTICULO` | number |  |
| `NUMERO DE CERTIFICADO` | number |  |
| `PARTES AFECTADAS` | multipleSelects | Options: PARTE DELANTERA, LATERALES, PARTE TRASERA, CRISTALES, NEUMATICOS, CERRADURAS, RUEDA DE AUXILIO, OTRAS PARTES |
| `FECHA DEL SINIESTRO` | date |  |
| `HORA APROX. DEL SINIESTRO` | duration |  |
| `LUGAR O ESTABLECIMIENTO` | multilineText |  |
| `DIRECCIÓN Y N°` | multilineText |  |
| `INTERSECCIÓN O ENTRE CALLES` | multilineText |  |
| `LOCALIDAD / PROV. / PAIS` | multilineText |  |
| `GOOGLE  MAPS URL` | aiText |  |
| `CODIGO POSTAL` | singleLineText |  |
| `TIPO DE CALLE` | singleSelect | Options: BOCACALLE, CALLE, RUTA, AVENIDA, OTRO, NINGUNA, ESTACIONAMIENTO PUBL / PRIV |
| `NOMBRE Y APELLIDO ( COND )` | singleLineText |  |
| `DNI ( COND )` | number |  |
| `DOMICILIO ( COND )` | singleLineText |  |
| `TELEFONO ( COND )` | phoneNumber |  |
| `FECHA DE NACIMIENTO (COND)` | date |  |
| `ESTADO CIVIL (COND)` | singleSelect | Options: CASADO, SOLTERO, SEPARADO/A, CONCUBINATO |
| `RELACIÓN CON EL ASEGURADO` | singleLineText |  |
| `ALCOHOLEMIA DEL CONDUCTOR` | singleSelect | Options: RESULTADO POSITIVO, RESULTADO NEGATIVO, SE NEGO, NO HUBO CONTROL, DESCONOCE, NINGUNO |
| `TIPO DE CONDUCTOR` | singleSelect | Options: HABITUAL, NO HABITUAL, NINGUNO |
| `LICENCIA CONDUCIR (COND)` | number |  |
| `EMISOR DE LICENCIA (COND)` | richText |  |
| `FECHA EMISIÓN (COND)` | date |  |
| `FECHA VENCIMIENTO (COND)` | date |  |
| `CATEGORIAS (COND)` | richText |  |
| `NOMBRE Y APELLIDO ( TER 1 )` | singleLineText |  |
| `DNI ( TER 1 )` | number |  |
| `TELEFONO ( TER 1 )` | phoneNumber |  |
| `MARCA DEL VEHICULO  ( TER 1 )` | singleLineText |  |
| `MODELO DEL VEHICULO ( TER 1 )` | singleLineText |  |
| `PATENTE ( TER 1 )` | singleLineText |  |
| `COMPAÑIA DE SEGURO ( TER 1 )` | singleSelect | Options: , ACA, AGRO SALTA, ALIANZ SEGUROS, ANTARTIDA, ATM, BERKLEY, COOPERACION SEGUROS, COPA SEGUROS, EL NORTE, FEDERACION PATRONAL, INTEGRITY, LA HOLANDO, LA SEGUNDA, LIBRA SEGUROS, LIDERAR, MAPFRE, MERCANTIL ANDINA, NACION SEGUROS, ORBIS, PARANA SEGUROS, PROTECCION, PROVIDENCIA, RIO URUGUAY, RIVADAVIA, SAN CRISTOBAL, SANCOR, SEGURO COOP, SEGURO LA EQUITATIVA, SEGURO METAL, SEGURO OESTE, SURA, SWISS MEDICAL SEGUROS, TRIUNFO SEGUROS, PROVINCIA, VICTORIA SEGUROS, ZURICH |
| `CLASIFICACIÓN DEL TERCERO ( TER 1 )` | singleSelect | Options: BICICLETA , PEATON, SIN DATOS DEL SEGURO, SIN DATOS DEL TERCERO, SIN SEGURO, TERCERO EN OTRA CIA, TERCERO EN TRIUNFO, TERCERO SE DA A LA FUGA |
| `HUBO DAÑOS A COSAS DE TERCERO (TER 1)` | singleSelect | Options: SI, NO |
| `HABIA ACOMPAÑANTES (TER 1)` | singleSelect | Options: SI, NO |
| `AFIRMATIVO - NOMBRE APELLIDO Y DNI DE LOS ACOMPAÑANTES (TER1)` | richText |  |
| `PRODUCTO LINK (de POLIZAS 2)` | rollup |  |
| `NOMBRE Y APELLIDO ( TER 2 )` | singleLineText |  |
| `DNI ( TER 2 )` | number |  |
| `TELEFONO ( TER 2 )` | phoneNumber |  |
| `MARCA DEL VEHICULO ( TER 2 )` | singleLineText |  |
| `MODELO DEL VEHICULO ( TER 2 )` | singleLineText |  |
| `PATENTE ( TER 2 )` | singleLineText |  |
| `COMPAÑIA DE SEGURO  ( TER 2 )` | singleSelect | Options: , ACA, AGROSALTA, ALLIANZ SEGUROS, ANTARTIDA, ATM, BERKLEY, COOPERACION SEGUROS, COPA SEGUROS, EL NORTE, FEDERACION PATRONAL, INTEGRITY, LA HOLANDO, LA SEGUNDA, LIBRA SEGUROS, LIDERAR, MAPRE, MERCANTIL ANDINA, NACION SEGUROS, ORBIS, PARANA SEGUROS, PROTECCION, PROVIDENCIA, RIO URUGUAY, RIVADAVIA, SAN CRISTOBAL, SANCOR, SEGURO LA EQUITATIVA, SEGURO METAL, SEGURO OESTE, SEGUROCOOP, SURA, SWISS MEDICAL SEGUROS, TRIUNFO SEGUROS, VICTORIA SEGUROS, ZURICH |
| `CLASIFICACIÓN DEL TERCERO ( TER 2 )` | singleSelect | Options: BICICLETA, PEATON, SIN DATOS DEL SEGURO, SIN DATOS DEL TERCERO, SIN SEGURO, TERCERO EN OTRA CIA, TERCERO EN TRIUNFO, TERCERO SE DA A LA FUGA |
| `HUBO DAÑOS A COSAS DE TERCERO (TER 2)` | singleSelect | Options: SI, NO |
| `HABIA ACOMPAÑANTES (TER 2)` | singleSelect | Options: SI, NO |
| `AFIRMATIVO - NOMBRE APELLIDO Y DNI DE LOS ACOMPAÑANTES (TER2)` | richText |  |
| `RELATOS DEL HECHO` | multilineText |  |
| `TIPO DE CALZADA` | singleSelect | Options: PAVIMENTADA, TIERRA, NINGUNO, CONSOLIDADO |
| `ESTADO DE CALZADA` | singleSelect | Options: BUENO, REGULAR, MALO, HIELO, RESBALADIZO, NINGUNO |
| `ESTADO DEL TIEMPO` | singleSelect | Options: SECO, LLUVIA, NIEBLA, GRANIZO, NIEVE, NINGUNO |
| `SENTIDO DE CIRCULACION` | singleSelect | Options: ESTACIONADO, NORTE - SUR, SUR - NORTE, ESTE - OESTE, OESTE - ESTE, DESCONOCE, NINGUNO |
| `HUBO IMPACTO` | singleSelect | Options: SI, NO |
| `SENTIDO CIRCULACIÓN DEL OTRO VEHICULO` | singleSelect | Options: ESTACIONADO, NORTE - SUR, SUR - NORTE, ESTE - OESTE, OESTE - ESTE, DESCONOCE, NINGUNO |
| `SEÑALES DE TRANSITO` | singleSelect | Options: CARTELES, VALLADO, REDUCTORES, OBSTACULO, OTROS |
| `HABIA SEMAFOROS` | multipleSelects | Options: SI, NO, VERDE, AMARILLO, ROJO, INTERMITENTE, NO RECUERDA, NO FUNCIONABA, NINGUNO |
| `DISTANCIA ENTRE VEHICULOS (METROS)` | singleSelect | Options: 1 METRO, 2 METROS, 3 METROS, 4 METROS, 5 METROS, 6 METROS, 7 METROS, 8 METROS, 9 METROS, 10 METROS, + 10 METROS |
| `PERSONAS EN VEHICULO (INCLUIDO CONDUCTOR)` | singleSelect | Options: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, + 10 |
| `TIPO DE COMBUSTIBLE` | singleSelect | Options: GNC, NAFTA, GASOIL, NINGUNA, NO APLICA |
| `USO DEL VEHICULO` | singleSelect | Options: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES, REPARTO-DELIVERY, TRANSPORTE DE BIENES, OFICIAL, AMBULANCIA, TRABAJO RURAL, VEHICULO DE ALQUILER SIN CHOFER, REMIS-TAXI, AUXILIO MECANICO, TRABAJO NO RURAL, NINGUNO |
| `TESTIGOS PRESENTES EN EL MOMENTO DEL HECHO` | singleSelect | Options: SI, NO |
| `DATOS TESTIGOS - NOMBRE Y APELLIDO` | singleLineText |  |
| `DNI DEL TESTIGO` | number |  |
| `DATOS TESTIGOS - DOMICILIO` | singleLineText |  |
| `DATOS TESTIGOS - TELEFONO` | phoneNumber |  |
| `DENUNCIA ANTE AUTORIDAD` | singleSelect | Options: SI, NO |
| `CLASIFICACIÓN` | singleSelect | Options: CON LESIONES, SIN LESIONES, GRANIZO, SI, NO |
| `NOMBRE Y APELLIDO DEL LESIONADO` | singleLineText |  |
| `DNI DEL LESIONADO` | singleLineText |  |
| `LESION MORTAL` | singleSelect | Options: SI, NO |
| `TRASLADO POR MEDIOS PROPIOS` | singleSelect | Options: SI, NO |
| `MEDIO DE  TRASLADO` | singleSelect | Options: AMBULANCIA, VEHICULO PARTICULAR, NINGUNO |
| `CENTRO DE INTERNACION` | multilineText |  |
| `ESTA INTERNADO` | singleSelect | Options: NO, SI |
| `DESCRIPCIÓN DE LESIONES` | multilineText |  |
| `FOTO DNI AMBOS LADOS` | multipleAttachments |  |
| `FOTO CEDULA VERDE AMBOS LADOS` | multipleAttachments |  |
| `FOTO CARNET CONDUCIR AMBOS LADOS` | multipleAttachments |  |
| `FOTO DAÑO DEL VEHICULO X 3` | multipleAttachments |  |
| `FOTO DE DENUNCIA OFICIAL ( EN CASO DE LESIONES )` | multipleAttachments |  |
| `RAZÓN SOCIAL DEL TALLER (T. RIESGO)` | singleLineText |  |
| `DOMICILIO TALLER (T. RIESGO)` | singleLineText |  |
| `TELEFONO TALLER (T. RIESGO)` | phoneNumber |  |
| `CULPABILIDAD IA` | aiText |  |
| `AGENTE 2: GESTOR DE PROTOCOLO` | aiText |  |
| `TRATAMIENTO` | singleSelect | Options: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO -A LA ESPERA DE RESPUESTA, NO REQUIERE TRATAMIENTO |
| `ESTADO DEL RECLAMOS` | singleSelect | Options: RESUELVE CON ABOGADO PERSONAL, RESUELVE CON ABOGADO NUESTRO, RESUELVE CON TALLER, RESUELVE PARTICULAR, DAÑOS MENORES-NO REALIZA ARREGLOS, DERIVADO AL GESTOR, DERIVADO A RUBEN MAURUTO |
| `OBSERVACIONES (DESTRUCCION TOTAL DETALLAR)` | richText |  |
| `NUMERO DE SINIESTRO` | singleLineText |  |
| `Estado_Gestion_AI` | singleSelect | Options: Nuevo, Formulario Enviado, Pendiente, En curso, Finalizado, Derivado a Humano |
| `Fecha_Derivacion` | dateTime |  |
| `Documentos_Pendientes` | richText |  |
| `Historial_Chat_AI` | multilineText |  |
| `URL_Audio` | url |  |
| `Transcripcion_Audio` | multilineText |  |
| `Chat_ID` | singleLineText |  |
| `Carga de Documentos` | singleLineText |  |
| `FOTO PERFIL (de CLIENTE)` | multipleLookupValues |  |
| `FECHA DE CREACION` | createdTime |  |
| `Checklist de documentación` | multipleSelects | Options: Denuncia policial, Copia DNI, Fotos del vehículo, Certificado médico, Presupuesto de reparación, Declaración jurada |
| `Estado del trámite` | singleSelect | Options: Iniciado, En proceso, Documentación completa, En revisión por aseguradora, Finalizado |
| `Fecha de última actualización` | dateTime |  |
| `Notas de seguimiento` | multilineText |  |
| `Responsable del seguimiento` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `datos adjunto portal cliente` | multipleAttachments |  |
| `ID_REGISTRO_CLIENTE_LOOKUP` | multipleLookupValues |  |
| `IR A CLIENTE` | button |  |
| `ESTADO_WEB` | singleSelect | Options: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `DICTAMEN_RESPONSABILIDAD` | formula | `IF(
  FIND("CULPABLE", UPPER({fldZ9duQSIRrQ5tM3})),
  "TRUE",
  IF(
    FIND("NO CULPABLE", UPPER({fldZ9duQSIRrQ5tM3})),
    "FALSE",
    "COMPLEJO"
  )
)` |
| `TIPO_COBERTURA` | formula | `IF(
  OR(
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TR",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "C",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "C1",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "C2",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "C2FULL",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TODORIESGO",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TODO RIESGO",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TERCEROSCOMPLETO PREMIUM",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TERCEROS COMPLETO PREMIUM",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "D",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "D1",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TR CON FRANQUICIA",
    UPPER(TRIM(ARRAYJOIN({fldMlJaRkA3yosLpI}, ""))) = "TRCONFRANQUICIA"
  ),
  "TR",
  "RC"
)` |
| `ID-GESTION-UNICO` | singleLineText |  |
| `NUMERO ID AUTOMATICO` | autoNumber |  |
| `CULPABILIDAD` | singleSelect | Options: CULPABLE, NO CULPABLE, VER TENGO DUDAS, CONCURRENCIA |
| `back uu CULPABILIDAD IA` | aiText |  |
| `Copia de CULPABILIDAD IA` | aiText |  |
| `Código` | multilineText |  |
| `GESTIÓN GENERAL 2` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `ID_UNICO_GESTION (from GESTIÓN GENERAL 2)` | multipleLookupValues |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `CLIENTES 2 (from POLIZAS)` | multipleLookupValues |  |
| `POLIZAS 2` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `N° CERTIFICADO (from POLIZAS 2)` | multipleLookupValues |  |
| `MARCA (from POLIZAS 2)` | multipleLookupValues |  |
| `MODELO (from POLIZAS 2)` | multipleLookupValues |  |
| `AÑO DEL VEHICULO (from POLIZAS 2)` | multipleLookupValues |  |
| `Seleccionar` | singleSelect | Options: ES EL ASEGURADO, NO ES EL ASEGURADO |
| `Creado por` | createdBy |  |

---

## 📄 DENUNCIA ROBO OC
(  CRISTALES, CERRADURAS, BATERIA, RUEDAS )

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_UNICO_GESTION` | formula | `{fldnO2OVcgjrkhqxZ} & "/" & {fldHUZWssgXc9qrIu} & "DOC🟠"` |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `ESCRIBE TÚ ID` | singleLineText |  |
| `ATENDIDO X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `CARGADA EN CIA X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `OFICINAS` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `TIPO DE ATENCIÓN` | singleSelect | Options: PRESENCIAL, WAPP-PERSONAL, 0810-AUTO-GESTIÓN, WLVX, VÍA E-MAIL, AGENTE IA, AUTO GESTIÓN WEB |
| `MOTIVOS DE LA CONSULTA` | singleSelect | Options: SINIESTRO, NO SINIESTRO |
| `PRODUCTO` | multipleLookupValues |  |
| `TIPO DE PRODUCTOS` | rollup |  |
| `CLIENTE` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DNI (from CLIENTE)` | multipleLookupValues |  |
| `TELEFONO  CLIENTE` | multipleLookupValues |  |
| `EMAIL CLIENTE` | multipleLookupValues |  |
| `MARCA DEL VEHICULO Compilación (de N° POLIZA)` | rollup |  |
| `MODELO DEL VEHICULO` | rollup |  |
| `AÑO DEL VEHICULO` | rollup |  |
| `PATENTE DEL VEHICULO (de GESTIÓN GENERAL) (from CLIENTES) Compilación (de N° POLIZA)` | rollup |  |
| `COBERTURA` | rollup |  |
| `CLASIFICACIÓN DE ADICIONALES` | singleSelect | Options: CON ADICIONAL CRISTALES, YA INCLUYE EN COBERTURA, CON ADICIONAL CUBIERTAS, SIN ADICIONAL CUBIERTAS, SIN ADICIONAL BATERIAS, CON ADICIONAL CERRADURAS, SIN ADICIONAL CRISTALES, SIN ADICIONAL CERRADURAS, CON ADICIONAL CUBIERTA |
| `ALCANCE DE COBERTURA` | singleSelect | Options: ESTÁ CUBIERTO, NO ESTÁ CUBIERTO |
| `CÓDIGO EMISÍON DE PÓLIZA` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `ARTICULO` | rollup |  |
| `CERTIFICADO` | rollup |  |
| `FECHA DEL SINIESTRO` | date |  |
| `HORA APROX. DEL SINIESTRO` | duration |  |
| `LUGAR O ESTABLECIMIENTO` | richText |  |
| `INTERSECCIÓN O ENTRE CALLES` | multilineText |  |
| `LOCALIDAD / PROV. / PAIS` | multilineText |  |
| `CÓDIGO POSTAL` | singleLineText |  |
| `Google Maps URL` | aiText |  |
| `N° POLIZA` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `N° DE POLIZA` | rollup |  |
| `ID_UNICO_CLIENTE` | multipleLookupValues |  |
| `DIRECCIÓN Y N°` | singleLineText |  |
| `NOMBRE Y APELLIDO ( DENU )` | singleLineText |  |
| `DNI ( DENU )` | number |  |
| `TELEFONO ( DENU )` | phoneNumber |  |
| `DOMICILIO ( DENU )` | multilineText |  |
| `FECHA DE NACIMIENTO (DENU)` | date |  |
| `ESTADO CIVIL ( DENU )` | singleSelect | Options: CONCUBINATO, SOLTERO, CASADO, SEPARADO, VIUDO/A |
| `RELACIÓN CON EL ASEGURADO` | singleLineText |  |
| `RELATOS DEL HECHO` | multilineText |  |
| `CLASIFICACIÓN DEL DAÑO` | multipleSelects | Options: PARABRISAS, LUNETA TRASERA, LATERAL DELANTERO, LATERAL TRASERO, VIDRIO FIJO LATERAL, VENTILETE, TECHO SOLAR (QUEMACOCO), TECHO PANORÁMICO, LUNETA LATERAL, CERRADURA BAÚL, CERRADURA LATERAL, ROBO BATERÍA, ROBO 1 RUEDA, ROBO 2 RUEDAS, ROBO 3 RUEDAS, ROBO 4 RUEDAS, ROBO RUEDA AUXILIAR, CRISTAL, CERRADURA |
| `DEJA CON FRECUENCIA VEHÍCULO AQUÍ` | singleSelect | Options: SÍ, NO |
| `TENÍA ALARMA ACTIVADA` | singleSelect | Options: SÍ, NO, NO TIENE ALARMA |
| `USO DEL VEHÍCULO` | singleSelect | Options: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES, REPARTO-DELIVERY, TRANSPORTE DE BIENES, OFICIAL, AMBULANCIA, TRABAJO RURAL, VEHICULO DE ALQUILER SIN CHOFER, REMIS-TAXI, AUXILIO MECANICO, TRABAJO NO RURAL, NINGUNO |
| `TIPO DE LUGAR` | singleSelect | Options: PÚBLICO, PRIVADO |
| `TIENE CÁMARA DE SEGURIDAD` | singleSelect | Options: SÍ, NO |
| `HUBO TESTIGOS` | singleSelect | Options: SÍ, NO |
| `CANTIDAD DE RUEDAS ROBADAS` | singleSelect | Options: 1, 2, 3, 4, 5, 6, 7, 8 |
| `REALIZÓ LLAMADO AL 911` | singleSelect | Options: SÍ, NO |
| `REALIZÓ DENUNCIA POLICIAL` | singleSelect | Options: SÍ, NO |
| `FRECUENCIA DE USO DEL VEHÍCULO` | singleSelect | Options: DIARIO, VARIOS DÍAS POR SEMANA, UNA VEZ POR SEMANA, QUINCENAL, MENSUAL, OCASIONAL |
| `FOTO DNI` | multipleAttachments |  |
| `FOTO CEDULA VERDE` | multipleAttachments |  |
| `FOTO CARNET CONDUCIR` | multipleAttachments |  |
| `FOTO DAÑO DEL VEHICULO` | multipleAttachments |  |
| `FOTO DE DENUNCIA OFICIAL ( EN CASO DE ROBO )` | multipleAttachments |  |
| `FOTO DE DENUNCIA OFICIAL` | multipleAttachments |  |
| `FOTO FACTURA COMPRA DE BATERÍA ( EN CASO ROBO BATERÍA )` | multipleAttachments |  |
| `NUMERO DE SINIESTRO ` | singleLineText |  |
| `OBSERVACIONES` | multilineText |  |
| `ORDEN PEDIDA A CIA` | singleSelect | Options: SI, NO |
| `VERIFICACION DE ORDEN` | singleSelect | Options: ENVIADA AL ASEGURADO, NO LE LLEGO, SE LLAMO AL ASEGURADO, NO SE GESTIONA, REINTEGRO |
| `Checklist de documentación` | multipleSelects | Options: DNI, Título de propiedad, Denuncia policial, Fotos del daño, Constancia de compañía, Formulario de reclamo, Factura de reparación |
| `Estado del trámite` | singleSelect | Options: Nuevo, En revisión, Enviado a compañía, Faltan documentos, A la espera de respuesta, Finalizado |
| `Fecha de última actualización` | dateTime |  |
| `Notas de seguimiento` | multilineText |  |
| `Responsable del seguimiento` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `datos adjunto portal cliente` | multipleAttachments |  |
| `NOMBRE Y APELLIDO TESTIGO` | singleLineText |  |
| `DNI TESTIGO` | number |  |
| `DOMICILIO DEL TESTIGO` | multilineText |  |
| `TELEFONO TESTIGO` | phoneNumber |  |
| `TIPO DE CONSULTA` | multipleSelects | Options: ROBO DE BATERÍA, ROBO DE AUTO, ROBO DE ACCESORIOS, ROBO PARCIAL, INTENTO DE ROBO, DAÑO POR ROBO, ROBO DE CRISTALES, ROBO DE CUBIERTAS, OTROS |
| `TRATAMIENTO` | singleSelect | Options: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO -A LA ESPERA DE RESPUESTA, NO REQUIERE TRATAMIENTO |
| `IR A CLIENTE` | button |  |
| `ID_REGISTRO_CLIENTE_LOOKUP` | multipleLookupValues |  |
| `ESTADO_WEB` | singleSelect | Options: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `NUMERO` | autoNumber |  |
| `From field: N° POLIZA` | singleLineText |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `POLIZAS 2` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `PRODUCTO LINK (de POLIZAS 2)` | multipleLookupValues |  |

---

## 📄 DENUNCIA ROBO / INCENDIO
  TOTAL/PARCIAL

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_UNICO_GESTION` | formula | `CONCATENATE({fld0OBwDwHzdrkLgg}, "/", {fldd7FgvlODfVBfNg}, "DRI🟣")` |
| `IR A CLIENTE` | button |  |
| `ESTADO_WEB` | singleSelect | Options: 🆕 NUEVO WEB, 👀 VISTO, ✅ PROCESADO |
| `ESCRIBE TÚ ID` | singleLineText |  |
| `ATENDIDO X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `OFICINAS` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `TIPO DE ATENCIÓN` | singleSelect | Options: WAPP-PERSONAL, PRESENCIAL, 0810-AUTO-GESTIÓN, VÍA E-MAIL, WLVX, AUTO GESTIÓN WEB |
| `MOTIVOS DE LA CONSULTA` | singleSelect | Options: SINIESTRO |
| `TIPO DE PRODUCTOS` | singleSelect | Options: MOTO, AUTO, REMIS, CAUCIÓN, BICICLETA, TAXI |
| `PRODUCTO` | multipleLookupValues |  |
| `CARGADO EN CIA X` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `ID_UNICO_CLIENTE` | multipleLookupValues |  |
| `CLIENTE` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DNI (from CLIENTE)` | multipleLookupValues |  |
| `TELEFONO (from CLIENTE)` | multipleLookupValues |  |
| `EMAIL (from CLIENTE)` | multipleLookupValues |  |
| `MARCA DEL VEHICULO (Rollup)` | rollup |  |
| `MODELO DEL VEHICULO (Rollup)` | rollup |  |
| `AÑO DEL VEHICULO (Rollup)` | rollup |  |
| `PATENTE DEL VEHICULO (Rollup)` | rollup |  |
| `COBERTURA (Rollup)` | rollup |  |
| `ALCANCE DE COBERTURA` | singleSelect | Options: ESTA CUBIERTO, NO ESTA CUBIERTO |
| `CÓDIGO EMISÍON DE PÓLIZA` | multipleRecordLinks | Link to `tblDLIvG4bnW7UUMi` |
| `ARTICULO (Rollup)` | rollup |  |
| `CERTIFICADO (Rollup)` | rollup |  |
| `FECHA DEL SINIESTRO` | date |  |
| `HORA APROX.DELSINIESTRO` | duration |  |
| `DIRECCIÓN Y N°` | singleLineText |  |
| `LUGAR O ESTABLECIMIENTO` | multilineText |  |
| `INTERSECCIÓN O ENTRE CALLES` | multilineText |  |
| `LOCALIDAD / PROV. / PAIS` | multilineText |  |
| `CÓDIGO POSTAL` | singleLineText |  |
| `Google Maps URL` | aiText |  |
| `NOMBRE Y APELLIDO ( DENU )` | singleLineText |  |
| `DNI ( DENU )` | number |  |
| `TELEFONO ( DENU )` | phoneNumber |  |
| `DOMICILIO ( DENU )` | singleLineText |  |
| `FECHA DE NACIMIENTO` | date |  |
| `ESTADO CIVIL` | singleSelect | Options: CONCUBINATO, SOLTERO, CASADO, SEPARADO/A, VIUDO/A |
| `RELACIÓN CON EL ASEGURADO` | singleLineText |  |
| `RELATOS DEL HECHO` | multilineText |  |
| `CLASIFICACIÓN DEL SINIESTRO` | singleSelect | Options: ROBO TOTAL, INCENDIO PARCIAL, DESTRUCCIÓN TOTAL, DAÑO PARCIAL-TODO RIESGO, INCENDIO TOTAL |
| `ROBO TOTAL (HALLAZGO)` | singleSelect | Options: SI, NO |
| `INCENDIO (INTERVENCIÓN BOMBEROS)` | singleSelect | Options: SI, NO |
| `SINIESTRO (FUERZA MAYOR)` | singleSelect | Options: SI, NO |
| `AFIRMATIVO (DESCRIBIR)` | multilineText |  |
| `USO DEL VEHICULO` | singleSelect | Options: COMERCIAL, PARTICULAR, SERVICIOS ESPECIALES, REPARTO-DELIVERY, TRANSPORTE DE BIENES, OFICIAL, AMBULANCIA, TRABAJO RURAL, VEHICULO DE ALQUILER SIN CHOFER, REMIS-TAXI, AUXILIO MECANICO, TRABAJO NO RURAL, NINGUNO |
| `DAÑOS A  TERCEROS` | singleSelect | Options: SI, NO |
| `AFIRMATIVO (Nombre, Apellido, DNI)` | multilineText |  |
| `HUBO LESIONADOS` | singleSelect | Options: SI, NO |
| `AFIRMATIVO LESIONADOS (Nombre, Apellido, DNI)` | multilineText |  |
| `LESION MORTAL` | singleSelect | Options: SI, NO |
| `SE RETIRO POR MEDIOS PROPIOS` | singleSelect | Options: SI, NO |
| `COMO FUE TRASLADADO` | singleSelect | Options: AMULANCIA, VEHICULO PARTICULAR, NINGUNO |
| `SE ENCUENTRA INTERNADO` | singleSelect | Options: SI, NO |
| `CENTRO DE INTERNACIÓN` | singleLineText |  |
| `DESCRIPCIÓN DE LA LESIÓN` | multilineText |  |
| `FOTO DNI` | multipleAttachments |  |
| `FOTO CEDULA VERDE` | multipleAttachments |  |
| `FOTO CARNET CONDUCIR` | multipleAttachments |  |
| `FOTO DAÑO DEL VEHICULO` | multipleAttachments |  |
| `FOTO DE DENUNCIA OFICIAL` | multipleAttachments |  |
| `FOTO  ACTA DE BOMBERO ( EN CASO DE iNCENDIO )` | multipleAttachments |  |
| `RAZON SOCIAL DEL TALLER` | multilineText |  |
| `DOMICILIO` | singleLineText |  |
| `TELEFONO 2` | phoneNumber |  |
| `ESTADO DE LA POLIZA` | singleSelect | Options: VIGENTE, ANULADA |
| `ESTADO DEL RECLAMO` | singleSelect | Options: RESUELVE CON ABOGADO PERSONAL, RESUELVE CON ABOGADO NUESTRO, RESUELVE CON TALLER, RESUELVE PARTICULAR, DAÑOS MENORES NO REALIZA ARREGLOS, DERIVADO AL GESTOR, DERIVADO A RUBEN MAURUTO |
| `TRATAMIENTO` | singleSelect | Options: YA FUE ASESORADO-FINALIZADO, ESTA SIENDO ASESORADO-EN PROCESO, YA FUE CONTACTADO-A LA ESPERA DE RESPUESTA, NO REQUIERE TRATAMIENTO |
| `OBSERVACIONES` | multilineText |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `TIPO DE CONSULTA` | multipleSelects | Options: ROBO , INCENDIO |
| `DEJA CON FRECUENCIA VEHÍCULO AQUÍ` | singleSelect | Options: SÍ, NO |
| `TENÍA ALARMA ACTIVADA` | singleSelect | Options: SÍ, NO |
| `TIPO DE LUGAR` | singleSelect | Options: PÚBLICO, PRIVADO |
| `TIENE CÁMARA DE SEGURIDAD` | singleSelect | Options: SÍ, NO |
| `HUBO TESTIGOS` | singleSelect | Options: SI, NO |
| `N° POLIZA` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `N° DE POLIZA (Rollup)` | rollup |  |
| `PRODUCTO LINK` | multipleRecordLinks | Link to `tblB06Eo9ep7PhCU6` |
| `TIPO DE PRODUCTOS (Rollup)` | rollup |  |
| `FRECUENCIA DEL VEHÍCULO` | singleSelect | Options: DIARIA, SEMANAL, MENSUAL, OCASIONAL |
| `NUMERO` | autoNumber |  |
| `datos adjunto portal cliente` | multipleAttachments |  |
| `ID_REGISTRO_CLIENTE_LOOKUP` | multipleLookupValues |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |

---

## 📄 PRIMA CALCULADA
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `NUMERO DE POLIZA` | autoNumber |  |
| `NOMBRE DEL CLIENTE` | singleLineText |  |
| `PRIMA SUGERIDA` | richText |  |
| `RECOMENDACION DE POLIZA` | richText |  |
| `JUSTIFICACION` | richText |  |
| `STATUS` | singleSelect | Options: EN REVISION, ENVIADO, ACEPTADO, NO ACEPTADO |
| `CLIENTE (relación)` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `DNI (de CLIENTE)` | multipleLookupValues |  |
| `TELEFONO (de CLIENTE)` | multipleLookupValues |  |
| `EMAIL (de CLIENTE)` | multipleLookupValues |  |
| `ID UNICO CLIENTE (de CLIENTE)` | multipleLookupValues |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |

---

## 📄 NUEVA TABLA
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `CODIGO DE POLIZA` | singleLineText |  |
| `NOMBRE Y APELLIDO` | singleLineText |  |
| `CORREO ELECTRONICO` | email |  |
| `FOTO DEL SINIESTRO` | multipleAttachments |  |
| `CLIENTE` | singleLineText |  |
| `DNI (CLIENTE)` | multipleLookupValues |  |
| `TELEFONO (CLIENTE)` | multipleLookupValues |  |
| `EMAIL (CLIENTE)` | multipleLookupValues |  |
| `ID UNICO CLIENTE (CLIENTE)` | multipleLookupValues |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |

---

## 📄 TRAZABILIDAD/IA
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID/TRAZABILIDAD` | formula | `IF(
  {fldHEWhD4YpgGjtuo},
  {fldHEWhD4YpgGjtuo} & "/TRAZ" & {fldA5A2M8hqHVI1Yd},
  BLANK()
)` |
| `Última modificación` | lastModifiedTime |  |
| `Fecha y Hora de Creación (Automática)` | createdTime |  |
| `ID_UNICO_CLIENTE` | singleLineText |  |
| `ID_GESTION_UNICO` | singleLineText |  |
| `Tipo de interacción` | singleSelect | Options: Nueva denuncia, Consulta estado, Documentación, Derivación, Recordatorio, Otro, Reclamo, Nuevo Clente, Actualizacion Cliente |
| `Interacción Resultado` | singleSelect | Options: Formulario enviado, En proceso, Pendiente, Finalizado, Derivado, Otro, Formulario recibido |
| `Notas` | multilineText |  |
| `Agente Responsable` | singleSelect | Options: Manual, Agente Virtual BledSRL |
| `Canal de Contacto` | singleSelect | Options: Teléfono, Email, WhatsApp, Web, Presencial, Otro |
| `Adjuntos de Interacción` | multipleAttachments |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `ID_TRAZABILIDAD` | autoNumber |  |

---

## 📄 CARGA DE DOCUMENTOS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID_GESTION_UNICO` | singleLineText |  |
| `ESTADO` | singleSelect | Options: Pendiente, Procesado |
| `FOTO DNI` | multipleAttachments |  |
| `FOTO CEDULA VERDE` | multipleAttachments |  |
| `FOTO CARNET CONDUCIR` | multipleAttachments |  |
| `FOTO DE DENUNCIA OFICIAL` | multipleAttachments |  |
| `FOTO DAÑO DEL VEHICULO` | multipleAttachments |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |

---

## 📄 COMPANIA
Tabla maestra de Aseguradoras con datos de contacto y auxilio para automatizaciones.

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `NOMBRE` | singleLineText |  |
| `LOGO` | multipleAttachments |  |
| `TEL. AUXILIO` | phoneNumber |  |
| `TEL. SINIESTROS` | phoneNumber |  |
| `EMAIL SINIESTROS` | email |  |
| `PORTAL PRODUCTORES` | url |  |
| `CUIT` | singleLineText |  |
| `EJECUTIVO DE CUENTA` | singleLineText |  |
| `NOTAS INTERNAS` | richText |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `PRODUCTO LINK` | multipleRecordLinks | Link to `tblB06Eo9ep7PhCU6` |
| `GESTIÓN GENERAL` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `Recuento (POLIZAS)` | count |  |

---

## 📄 PRODUCTOS
Tabla maestra de Tipos de Productos (Ramos) para clasificar pólizas y compañías.

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `NOMBRE PRODUCTO` | singleLineText |  |
| `ICONO` | singleLineText |  |
| `DESCRIPCION` | richText |  |
| `COMPANIA` | multipleRecordLinks | Link to `tbl8jENHY2lESAA5b` |
| `COBERTURAS DISPONIBLES` | richText |  |
| `POLIZAS` | multipleRecordLinks | Link to `tblEpvdJAQCA7wUe9` |
| `Recuento (POLIZAS)` | count |  |
| `DENUNCIA ROBO / INCENDIO` | multipleRecordLinks | Link to `tblLnVFRONjVZ7YUH` |
| `GESTIÓN GENERAL 2` | multipleRecordLinks | Link to `tblA4AV8Lp7OvaUzI` |
| `DENUNCIA ROBO OC` | singleLineText |  |

---

## 📄 LOGIN
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `EMAIL` | email |  |
| `CONTRASEÑA` | singleLineText |  |
| `ROL` | singleSelect | Options: Empleado, Gerente, Dueño, Visitante |
| `ROL OPERATIVO` | formula | `TRIM({fld1P86jVMhICO9eA} & "")` |
| `ESTADO` | singleSelect | Options: Activo, Inactivo, Pendiente |
| `URL_PORTAL` | formula | `IF(
  {fldMt4uWj6v1mJcCK} = "Activo",
  SWITCH(
    {fld1P86jVMhICO9eA},
    "Dueño", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    "Gerente", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    "Empleado", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    ""
  ),
  ""
)` |
| `EMPLEADO` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `NOMBRE Y APELLIDO` | formula | `UPPER(CONCATENATE({fldBIZajRtb17tb8f}, " ", {fldJWI7aXH7ePgVmx}))` |
| `NOMBRE` | singleLineText |  |
| `APELLIDO` | singleLineText |  |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIIFICACION` | lastModifiedTime |  |

---

## 📄 PORTAL
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID` | autoNumber |  |
| `ROL` | multipleSelects | Options: EMPLEADO, GERENTE, DUEÑO |
| `FRASES DEL PORTAL` | aiText |  |
| `FOTOS DEL PORTAL` | multipleAttachments |  |

---

## 📄 TOKENS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `TOKEN` | singleLineText |  |
| `URL_DESTINO` | url |  |
| `EXPIRA` | singleLineText |  |
| `USADO` | checkbox |  |
| `EMAIL_USUARIO` | singleLineText |  |

---

## 📄 CALIFICACIONES
Calificaciones de clientes - Rating dinámico para Linktree

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ESTRELLAS` | number |  |
| `NOMBRE` | singleLineText |  |
| `ES_CLIENTE` | singleSelect | Options: Sí, No |
| `DNI` | number |  |
| `SERVICIO` | singleSelect | Options: Atención General, Cotización, Siniestro, Gestión de Póliza |
| `COMENTARIO` | multilineText |  |
| `MODO` | singleSelect | Options: Online, Presencial |
| `VISIBLE` | checkbox |  |
| `EMPLEADO` | multipleRecordLinks | Link to `tblNbE8QOcNyutnbt` |
| `CLIENTE` | multipleRecordLinks | Link to `tblVAcMxNTLYXbLfT` |
| `FOTO PERFIL` | multipleLookupValues |  |
| `CUAL FUE TU EXPERIENCIA CON NOSOTROS` | rating |  |
| `URGENCIA DE ATENCION (AI)` | singleSelect | Options: Atender urgente, Próximo a contactar, Calificación cerrada |
| `FECHA DE CREACION` | createdTime |  |
| `ULTIMA MODIFICACION` | lastModifiedTime |  |
| `AUTORIZA_PUBLICAR` | checkbox |  |
| `USAR FOTO` | checkbox |  |

---

## 📄 BIBLIOTECA_AUDIOS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `CODIGO_ID` | singleLineText |  |
| `ARCHIVO_AUDIO` | multipleAttachments |  |
| `ASUNTO_EMAIL` | singleLineText |  |
| `CUERPO_EMAIL` | richText |  |
| `DESCRIPCION_INTERNA` | singleLineText |  |
| `URL_PUBLICA` | formula | `IF(
  {fldTv7GKGytE8sRQd},
  {fldTv7GKGytE8sRQd}
)` |
| `CREADO_POR` | createdBy |  |
| `FECHA_CREACION` | createdTime |  |
| `FECHA_ULTIMA_MODIFICACION` | lastModifiedTime |  |
| `VISIBLE_A_CLIENTES` | checkbox |  |

---

## 📄 CONFIG_FORMULARIOS
Configuración dinámica de formularios para la App de Seguros

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `CODIGO` | singleLineText |  |
| `TITULO` | singleLineText |  |
| `ICONO` | singleLineText |  |
| `COLOR` | singleLineText |  |
| `CONFIG_CAMPOS` | multipleRecordLinks | Link to `tblBJoFWFZxHo8zpq` |
| `TABLA RELACIONADA` | singleLineText |  |
| `VISIBILIDAD` | checkbox |  |

---

## 📄 CONFIG_CAMPOS
Campos de los formularios dinámicos

### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `ID CAMPO` | singleLineText |  |
| `ETIQUETA` | singleLineText |  |
| `TIPO` | singleSelect | Options: Single line text (Texto de una línea), Long text (Texto largo), Rich text (Texto con formato), Number (Número), Currency (Moneda), Percent (Porcentaje), Rating (Calificación), Duration (Duración), Date (Fecha), Date and time (Fecha y hora), Single select (Selección única), Multiple select (Selección múltiple), Email, Phone number (Teléfono), URL, Attachment (Adjuntos), Linked record (Registro vinculado), Lookup (Búsqueda), Rollup (Resumen), User (Usuario/Colaborador), Created by (Creado por), Last modified by (Modificado por), Autonumber (Autonumérico), Created time (Fecha de creación), Last modified time (Última modificación), Formula (Fórmula), Checkbox (Casilla de verificación), Barcode (Código de barras), Button (Botón), AI text (Texto IA), Texto de una sola linea, date, number, text, select, textarea, file |
| `OPCIONES` | multilineText |  |
| `OBLIGATORIO` | checkbox |  |
| `ORDEN` | number |  |
| `FORMULARIO` | multipleRecordLinks | Link to `tblbkMQlI9BpGQndA` |
| `COLUMNA AIRTABLE` | singleLineText |  |

---

## 📄 FAQ
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `PREGUNTA` | multilineText |  |
| `RESPUESTA` | multilineText |  |
| `CATEGORIA` | multilineText |  |
| `ORDEN` | number |  |
| `VISIBLE` | checkbox |  |
| `ICONO` | singleLineText |  |

---

## 📄 QUIENES_SOMOS
### 📌 Campos

| Campo | Tipo | Detalles / Fórmula |
| :--- | :--- | :--- |
| `TITULO` | multilineText |  |
| `SUBTITULO` | multilineText |  |
| `TEXTO PRINCIPAL` | multilineText |  |
| `NOMBRE RESPONSABLE` | singleLineText |  |
| `CARGO` | singleLineText |  |
| `FOTO PERFIL` | multipleAttachments |  |
| `ANIOS EXPERIENCIA` | number |  |
| `CANTIDAD CLIENTES` | number |  |
| `CANTIDAD SUCURSALES` | number |  |
| `CANTIDAD POLIZAS` | number |  |
| `MISION` | multilineText |  |
| `VISION` | multilineText |  |
| `VALORES` | multilineText |  |
| `IMAGEN FONDO` | multipleAttachments |  |
| `COLOR PRINCIPAL` | singleLineText |  |
| `COLOR SECUNDARIO` | singleLineText |  |
| `VIDEO PRESENTACION` | url |  |
| `MOSTRAR ESTADISTICAS` | checkbox |  |
| `VISIBLE` | checkbox |  |

---

