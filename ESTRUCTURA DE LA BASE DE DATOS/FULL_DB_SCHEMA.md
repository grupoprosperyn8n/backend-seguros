# Sistema de Seguros Agénticos - Esquema de Base de Datos Airtable
> **Base ID:** `appuhslj3GFf60Tea`
> **Estado:** API DEEP SCAN (Todas las tablas escaneadas en profundidad)
> **Fecha:** 2024-02-07

**REPORTE DE HALLAZGOS:**
Tras escanear los últimos 50 registros de cada tabla:
1.  **CAMPO "USO DEL VEHÍCULO" CONFIRMADO** en `DENUNCIA DE ACCIDENTE` (Tipo: Single Select).
2.  **NO SE ENCONTRÓ CAMPO DE "RUEDAS" O "MEDIDAS"** en `DENUNCIA ROBO OC`.
    *(Aunque existen métricas en 'EMPLEADOS' que cuentan 'RUEDAS', la tabla de detalle no mostró columna específica con datos).*
3.  **SOLUCIÓN IMPLEMENTADA:** Estos datos se guardan en `RELATOS DEL HECHO` para evitar pérdida de información.

---

## 🚘 DENUNCIA DE ACCIDENTE
Registra choques y granizo.

### 📌 Campos Confirmados
| Campo | Tipo Detectado |
| :--- | :--- |
| `ID_GESTION_UNICO` | String |
| `FECHA DEL SINIESTRO` | String |
| `HORA APROX. DEL SINIESTRO` | Number (Int) |
| `DIRECCIÓN Y N°` | String |
| `LUGAR O ESTABLECIMIENTO` | String |
| `INTERSECCIÓN O ENTRE CALLES` | String |
| `RELATOS DEL HECHO` | Date/DateTime (⚠️ Mapeado como String en n8n) |
| `CLASIFICACIÓN` | String |
| `CULPABILIDAD` | String |
| `CULPABILIDAD IA` | Object (JSON) |
| `Back uu CULPABILIDAD IA` | Object |
| `GOOGLE MAPS URL` | Object |
| `USO DEL VEHICULO` | Single Select (Opciones: PARTICULAR, COMERCIAL, REMIS-TAXI, SERVICIOS ESPECIALES, REPARTO-DELIVERY, etc.) |

### 🚗 Datos del Vehículo (Lookups)
| Campo | Tipo Detectado |
| :--- | :--- |
| `MARCA DEL VEHICULO` | String |
| `MODELO DEL  VEHICULO` | String |
| `AÑO DEL VEHICULO` | String |
| `PATENTE DEL VEHICULO` | List (Linked/Lookup) |

---

## 🔧 DENUNCIA ROBO OC
Registra robos parciales, ruedas, cristales.

### 📌 Campos Confirmados
| Campo | Tipo Detectado |
| :--- | :--- |
| `ID_UNICO_GESTION` | String |
| `FECHA DEL SINIESTRO` | String |
| `HORA APROX. DEL SINIESTRO` | Number (Int) |
| `DIRECCIÓN Y N°` | String |
| `RELATOS DEL HECHO` | Date/DateTime (⚠️ Mapeado como String en n8n) |
| `CLASIFICACIÓN DEL DAÑO` | List (Linked/Lookup) |
| `ALCANCE DE COBERTURA` | String |
| `MOTIVOS DE LA CONSULTA` | String |
| `CLASIFICACIÓN DE ADICIONALES` | String |
| `VERIFICACION DE ORDEN` | String |
| `ORDEN PEDIDA A CIA` | String |

---

## 👥 CLIENTES
Tabla maestra.

### 📌 Campos Confirmados
| Campo | Tipo Detectado |
| :--- | :--- |
| `ID_UNICO_CLIENTE` | String |
| `NOMBRES` | String |
| `APELLIDO` | String |
| `DNI` | Number (Int) |
| `TELEFONO` | String |
| `EMAIL` | String |
| `FECHA DE ALTA` | Date/DateTime |
| `✅ CANTIDAD_POLIZAS` | Number (Int) |
| `⭕ SIN_POLIZAS` | Number (Int) |
| `🔴 POLIZAS_ANULADAS` | Number (Int) |
| `🟢 POLIZAS_ACTIVAS` | Number (Int) |

---

## 📄 POLIZAS
Registro de pólizas.

### 📌 Campos Confirmados
| Campo | Tipo Detectado |
| :--- | :--- |
| `N° DE POLIZA` | String |
| `ETIQUETA_POLIZA` | String |
| `ESTADO DE LA POLIZA` | String |
| `MARCA DEL VEHICULO` | String |
| `MODELO DEL VEHICULO` | String |
| `AÑO DEL VEHICULO` | Number (Int) |
| `PATENTE DEL VEHICULO` | String |
| `AUXILIO` | String |

---

## 👨‍💼 EMPLEADOS
Staff y Métricas.

### 📌 Campos Confirmados
| Campo | Tipo Detectado |
| :--- | :--- |
| `NOMBRE Y APELLIDO` | String |
| `CUIL` | String |
| `EMAIL` | String |
| `FOTO DE PERFIL` | Attachment |
| `ROL OPERATIVO` | List (Linked/Lookup) |
| `Recuento (CARGA DENUNCIA OC ... RUEDAS )) ...` | Number (Int) (Múltiples métricas detectadas) |

---
*El resto de tablas (LOGIN, OFICINAS, COMPANIA, PRODUCTOS, GESTIÓN GENERAL) se mantienen consistentes con el reporte anterior.*
