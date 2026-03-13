# 📊 ANÁLISIS COMPLETO DE RELACIONES - AIRTABLE

Este documento detalla cómo se conectan las tablas y la lógica de negocio detrás de las fórmulas clave.

## 🔗 Grafo de Relaciones

### CLIENTES
- Conecta con `EMPLEADOS` a través del campo `EMPLEADOS`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `DENUNCIA DE ACCIDENTE`
- Conecta con `PRIMA CALCULADA` a través del campo `PRIMA CALCULADA`
- Conecta con `DENUNCIA ROBO OC` a través del campo `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 6`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2`
- Conecta con `OFICINAS` a través del campo `OFICINAS`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL`
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `CALIFICACIONES` a través del campo `CALIFICACIONES`

### EMPLEADOS
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `DENUNCIA DE ACCIDENTE`
- Conecta con `DENUNCIA ROBO OC` a través del campo `DENUNCIA ROBO OC`
- Conecta con `LOGIN` a través del campo `Login`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTION GENERAL`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR )`
- Conecta con `DENUNCIA ROBO OC` a través del campo `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )`
- Conecta con `DENUNCIA ROBO OC` a través del campo `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 2`
- Conecta con `CLIENTES` a través del campo `CLIENTES`
- Conecta con `CALIFICACIONES` a través del campo `CALIFICACIONES`

### OFICINAS
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `CARGA DE DENUNCIA DE ACCIDENTE  MENSUAL`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `CARGA DE DENUNCIA DE ACCIDENTE ( SIRVE TAMBIEN PARA DT Y TR ) 2`
- Conecta con `DENUNCIA ROBO OC` a través del campo `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS )`
- Conecta con `DENUNCIA ROBO OC` a través del campo `CARGA DENUNCIA OC (  CRISTALES, CERRADURAS, BATERIA, RUEDAS ) 2`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL 2`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 3`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO TOTAL , INCENDIO  TOTAL/PARCIAL 4`
- Conecta con `CLIENTES` a través del campo `CLIENTES 2`

### GESTIÓN GENERAL
- Conecta con `CLIENTES` a través del campo `CLIENTE`
- Conecta con `OFICINAS` a través del campo `OFICINAS`
- Conecta con `PRODUCTOS` a través del campo `TIPO DE PRODUCTOS`
- Conecta con `EMPLEADOS` a través del campo `ATENDIDO X`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `DENUNCIA DE ACCIDENTE 2`
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `POLIZAS` a través del campo `N°  POLIZA GESTIONADA`
- Conecta con `COMPANIA` a través del campo `COMPANIA`

### POLIZAS
- Conecta con `GESTIÓN GENERAL` a través del campo `ACTIVAR POLIZA`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO / INCENDIO`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL`
- Conecta con `CLIENTES` a través del campo `CLIENTES 2`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `DENUNCIA DE ACCIDENTE`
- Conecta con `DENUNCIA DE ACCIDENTE` a través del campo `DENUNCIA DE ACCIDENTE 2`
- Conecta con `COMPANIA` a través del campo `COMPANIA LINK`
- Conecta con `PRODUCTOS` a través del campo `PRODUCTO LINK`
- Conecta con `DENUNCIA ROBO OC` a través del campo `DENUNCIA ROBO OC 3`
- Conecta con `DENUNCIA ROBO OC` a través del campo `DENUNCIA ROBO OC 4`
- Conecta con `DENUNCIA ROBO OC` a través del campo `DENUNCIA ROBO OC 5`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO / INCENDIO 2`

### DENUNCIA DE ACCIDENTE
- Conecta con `EMPLEADOS` a través del campo `ATENDIDO X`
- Conecta con `OFICINAS` a través del campo `OFICINAS`
- Conecta con `CLIENTES` a través del campo `CLIENTE`
- Conecta con `EMPLEADOS` a través del campo `CARGADO EN CIA X`
- Conecta con `OFICINAS` a través del campo `CODIGO EMISION DE LA POLIZA`
- Conecta con `EMPLEADOS` a través del campo `Responsable del seguimiento`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL 2`
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `POLIZAS` a través del campo `POLIZAS 2`

### DENUNCIA ROBO OC
- Conecta con `EMPLEADOS` a través del campo `ATENDIDO X`
- Conecta con `EMPLEADOS` a través del campo `CARGADA EN CIA X`
- Conecta con `OFICINAS` a través del campo `OFICINAS`
- Conecta con `CLIENTES` a través del campo `CLIENTE`
- Conecta con `OFICINAS` a través del campo `CÓDIGO EMISÍON DE PÓLIZA`
- Conecta con `POLIZAS` a través del campo `N° POLIZA`
- Conecta con `EMPLEADOS` a través del campo `Responsable del seguimiento`
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `POLIZAS` a través del campo `POLIZAS 2`

### DENUNCIA ROBO / INCENDIO
- Conecta con `EMPLEADOS` a través del campo `ATENDIDO X`
- Conecta con `OFICINAS` a través del campo `OFICINAS`
- Conecta con `EMPLEADOS` a través del campo `CARGADO EN CIA X`
- Conecta con `CLIENTES` a través del campo `CLIENTE`
- Conecta con `OFICINAS` a través del campo `CÓDIGO EMISÍON DE PÓLIZA`
- Conecta con `POLIZAS` a través del campo `N° POLIZA`
- Conecta con `PRODUCTOS` a través del campo `PRODUCTO LINK`
- Conecta con `POLIZAS` a través del campo `POLIZAS`

### PRIMA CALCULADA
- Conecta con `CLIENTES` a través del campo `CLIENTE (relación)`

### COMPANIA
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `PRODUCTOS` a través del campo `PRODUCTO LINK`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL`

### PRODUCTOS
- Conecta con `COMPANIA` a través del campo `COMPANIA`
- Conecta con `POLIZAS` a través del campo `POLIZAS`
- Conecta con `DENUNCIA ROBO / INCENDIO` a través del campo `DENUNCIA ROBO / INCENDIO`
- Conecta con `GESTIÓN GENERAL` a través del campo `GESTIÓN GENERAL 2`

### LOGIN
- Conecta con `EMPLEADOS` a través del campo `EMPLEADO`

### CALIFICACIONES
- Conecta con `EMPLEADOS` a través del campo `EMPLEADO`
- Conecta con `CLIENTES` a través del campo `CLIENTE`

### CONFIG_FORMULARIOS
- Conecta con `CONFIG_CAMPOS` a través del campo `CONFIG_CAMPOS`

### CONFIG_CAMPOS
- Conecta con `CONFIG_FORMULARIOS` a través del campo `FORMULARIO`

## 🧪 Fórmulas Críticas (Lógica de Negocio)

### CLIENTES
- **NOMBRE NORMALIZADO**: `SUBSTITUTE(
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
)`
- **🏷️ ESTADO_CLIENTE**: `REGEX_REPLACE(
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
)`
- **ID_UNICO_CLIENTE**: `"🆔 " & RIGHT(CONCATENATE({fldgfcpYGlVrRACcb}), 3) & UPPER(LEFT({fldzJskztOW1uotuc}, 3))`
- **ID_REGISTRO_CLIENTE**: `RECORD_ID()`

### EMPLEADOS
- **NOMBRE Y APELLIDO NORMALIZADO**: `UPPER({fldnLBeF1MB6KUdO4})`
- **ID_UNICO_EMPLEADO**: `CONCATENATE(
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
)`
- **Resumen Total Anual**: `"TOTAL DE GESTION GENERAL ANUAL: " & {fldyRnnow5QcV4Ca8} & "\n" &
"TOTAL DE ACCIDENTE ANUAL: " & {fldN9P1Yn2nwoNbhR} & "\n" &
"TOTAL DE ROBO INCENDIO ANUAL: " & {fldHd94xIHbCvO4HO} & "\n" &
"TOTAL DE ROBO OC ANUAL: " & {fld3A5q0DjI7CEJxe} & "\n" &
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" &
"TOTAL GENERAL ANUAL: " & (
  {fldyRnnow5QcV4Ca8} +
  {fldN9P1Yn2nwoNbhR} +
  {fldHd94xIHbCvO4HO} +
  {fld3A5q0DjI7CEJxe}
)`

### OFICINAS
- **NOMBRE_OFICINA_LIMPIO_WEB**: `TRIM(REGEX_REPLACE({fldbRydM9VwwRAkVD}, " ?\\([^\\)]*\\)", ""))`
- **Resumen Cantidades y Total General**: `"TOTAL DE GESTION GENERAL: " & {fldgtOOZUgcMNz54c} & "\n" &
"TOTAL DE ACCIDENTE: " & {fldYnnUeJobL2D9G6} & "\n" &
"TOTAL DE ROBO INCENDIO: " & {flduTUCAb2W3PSlig} & "\n" &
"TOTAL DE ROBO OC: " & {flde0gTUBSbzU34gm} & "\n" &
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" &
"TOTAL GENERAL: " & (
  {fldgtOOZUgcMNz54c} +
  {fldYnnUeJobL2D9G6} +
  {flduTUCAb2W3PSlig} +
  {flde0gTUBSbzU34gm}
)`

### GESTIÓN GENERAL
- **ID_UNICO_GESTION**: `CONCATENATE({fld0wPLry103yD2Il}, "/", {fldkcOLXVUX7NYc9b}, "GG🔵")`
- **COMISIÓN VIDA**: `{fldm4h2HWbR0KUuiz}`
- **💰 TOTAL COMISIÓN**: `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b8cNvoIKGwsbt}`
- **💰✅ TOTAL COMISIÓN FINAL**: `IF({fldTukq50AVcZM8Eu} = 'N CREDITO', {fldFTtvSdMa6eSNN7} + {fldm4h2HWbR0KUuiz}, {fldFTtvSdMa6eSNN7})`
- **🟠 ALERTA PAGO EN EFECTIVO**: `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', '🟠 Alerta: Pago en Efectivo', '')`
- **🔴 Aviso Comisión Cero**: `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8EbNtYgrelv} = 0, DATETIME_DIFF(TODAY(), {fldsitgCySZods6Il}, 'days') >= 30), '🔴 Comisión es 0', '')`
- **🔢✅ Cantidad de ALTAS**: `IF({fldQSvgctDcTZ9TXY} = 'ALTAS', 1, 0)`
- **🔢 ❌ Cantidad de ANULACIÓN**: `IF({fldQSvgctDcTZ9TXY} = 'ANULACIÓN', 1, 0)`
- **🔢 ✳️Diferencia ALTAS-ANULACIÓN**: `{fldSspNQJl5SPV40x} - {fld5oogxxETzlGnRg}`
- **JAJAJA**: `IF(OR({fldi0omqIDbHpxO1O} > 0, {fld2b8cNvoIKGwsbt} > 0), {fldtCYI9REtFaInLB} * 0.08, IF(AND({fldi0omqIDbHpxO1O} = 0, {fld2b8cNvoIKGwsbt} = 0), {fldtCYI9REtFaInLB} * 0.02, 0))`
- **💼 COMISIÓN VIDA + JAJAJA**: `{fldi0omqIDbHpxO1O} + {fldn734Iq6YJKVMV0}`
- **COMISIÓN AUX**: `{fldtcTWSS2ffbzuZ7} / 2`
- **COMISIÓN AUX + JAJAJA**: `{fld2b8cNvoIKGwsbt} + {fldn734Iq6YJKVMV0}`
- **💵 COMISIÓN ALTA SIMPLE**: `{fldtCYI9REtFaInLB} * 0.02`
- **💲 TOTAL COMI COMBINADAS**: `{fldn734Iq6YJKVMV0} + {fldi0omqIDbHpxO1O} + {fld2b8cNvoIKGwsbt}`
- **✅💰 TOTAL COMISIÓN FINAL 1**: `IF({fldQSvgctDcTZ9TXY} != 'ALTAS', 0, {fldanV8EbNtYgrelv})`
- **💰 TOTAL COMISIÓN AJUSTADA**: `IF({fldfpGPml5Opd8CtT} = 'EFECTIVO', 0, {fldmhPEfrraHkRiuU})`
- **Copia de 🔴 Aviso Comisión Cero**: `IF(AND({fldfpGPml5Opd8CtT} = 'EFECTIVO', {fldanV8EbNtYgrelv} = 0, DATETIME_DIFF(NOW(), {fldsitgCySZods6Il}, 'minutes') >= 5), '🔴 Comisión es 0', '')`

### POLIZAS
- **ETIQUETA_POLIZA**: `UPPER(
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
)`

### DENUNCIA DE ACCIDENTE
- **ID_GESTION_UNICO**: `CONCATENATE(
  ARRAYJOIN({fldLrTr9OUePj5eER}, ""),
  "/",
  {fldXtfy3gY4QD5jzI},
  "CDA🔴"
)`
- **DICTAMEN_RESPONSABILIDAD**: `IF(
  FIND("CULPABLE", UPPER({fldZ9duQSIRrQ5tM3})),
  "TRUE",
  IF(
    FIND("NO CULPABLE", UPPER({fldZ9duQSIRrQ5tM3})),
    "FALSE",
    "COMPLEJO"
  )
)`
- **TIPO_COBERTURA**: `IF(
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
)`

### DENUNCIA ROBO OC
- **ID_UNICO_GESTION**: `{fldnO2OVcgjrkhqxZ} & "/" & {fldHUZWssgXc9qrIu} & "DOC🟠"`

### DENUNCIA ROBO / INCENDIO
- **ID_UNICO_GESTION**: `CONCATENATE({fld0OBwDwHzdrkLgg}, "/", {fldd7FgvlODfVBfNg}, "DRI🟣")`

### TRAZABILIDAD/IA
- **ID/TRAZABILIDAD**: `IF(
  {fldHEWhD4YpgGjtuo},
  {fldHEWhD4YpgGjtuo} & "/TRAZ" & {fldA5A2M8hqHVI1Yd},
  BLANK()
)`

### LOGIN
- **ROL OPERATIVO**: `TRIM({fld1P86jVMhICO9eA} & "")`
- **URL_PORTAL**: `IF(
  {fldMt4uWj6v1mJcCK} = "Activo",
  SWITCH(
    {fld1P86jVMhICO9eA},
    "Dueño", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    "Gerente", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    "Empleado", "https://airtable.com/appuhslj3GFf60Tea/pagZyBnfXRNqcQ4Jn/preview",
    ""
  ),
  ""
)`
- **NOMBRE Y APELLIDO**: `UPPER(CONCATENATE({fldBIZajRtb17tb8f}, " ", {fldJWI7aXH7ePgVmx}))`

### BIBLIOTECA_AUDIOS
- **URL_PUBLICA**: `IF(
  {fldTv7GKGytE8sRQd},
  {fldTv7GKGytE8sRQd}
)`

