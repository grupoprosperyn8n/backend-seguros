# Memoria del Proyecto - Sistema de Seguros Agénticos

> **Cliente:** Rafael Allende & Asociados Seguros
> **Inicio:** 2026-02-04
> **Estado:** 🟢 Producción Activa (Backend Python v1.0)

---

## Resumen del Sistema

Sistema de gestión inteligente para una compañía de seguros. Incluye autenticación por roles, portal personalizado, y backend python de alto rendimiento.

---

## Componentes Principales

### 1. SaaS-Login

Portal de autenticación con:

- Login con credenciales validadas contra Airtable
- Registro de nuevos usuarios (requiere aprobación)
- Sistema de tokens temporales (URL masking)
- Redirección por rol a diferentes interfaces de Airtable

**URLs Producción:**

| Servicio | URL |
|----------|-----|
| Login | https://login-agentico-1770227340.surge.sh |
| Registro | https://registro-agentico-1770227370.surge.sh |
| Linktree | https://seguros_linktree.surge.sh |
| Backend API | https://web-production-2584d.up.railway.app |

---

## Arquitectura Técnica

```
┌──────────────┐     ┌─────────────┐     ┌───────────────┐
│   Frontend   │────▶│   Python    │────▶│   Airtable    │
│  (Surge.sh)  │     │  (FastAPI)  │     │  (Base datos) │
└──────────────┘     └─────────────┘     └───────────────┘
       │                    │
       │                    ▼
       │            ┌─────────────┐
       └───────────▶│   Airtable  │
                    │  Interface  │
                    └─────────────┘
```

---

## Tablas de Airtable

**Base ID:** `appuhslj3GFf60Tea`

| Tabla | Propósito |
|-------|-----------|
| `USUARIOS` | Credenciales y datos de usuarios |
| `PORTAL CONTENIDO` | Contenido por rol (frases, imágenes) |
| `Tokens` | Tokens temporales para URL masking |
| `CALIFICACIONES` | Testimonios y Ratings |
| `CLIENTES` | Validación de Pólizas y Siniestros |

---

## Backend Python (FastAPI)

Reemplazo de workflows complejos de n8n por código Python determinista.

| Endpoint | Método | Función |
|----------|--------|---------|
| `/api/validar-cliente` | GET | Valida DNI + Patente contra Airtable |
| `/api/testimonios` | GET | Obtiene testimonios (Lógica 70/30, prioridad 3 meses) |
| `/api/rating` | GET | Calcula promedio de estrellas visibles |
| `/api/rating` | POST | Guarda nueva calificación |
| `/api/siniestro` | POST | Recibe reporte de siniestro |

---

## Credenciales y Tokens

> ⚠️ **CONFIDENCIAL - No compartir**

| Servicio | Credencial |
|----------|------------|
| Airtable API | `patSnkbIu2xq3v45g...` (En Variables de Entorno Railway) |
| Backend Base URL | `https://web-production-2584d.up.railway.app` |

---

## 🧪 Datos de Prueba (QA)

Utilizar siempre estos datos para verificar flujos de extremo a extremo:

| Campo | Valor | Notas |
|-------|-------|-------|
| **Usuario** | DIEGO LOPEZ | Cliente real de prueba |
| **DNI** | `26322995` | Documento vinculado |
| **Patente** | `PDL384` | Vehículo registrado |
| **Caso Uso** | Siniestro Choque / Robo | Probar carga de adjuntos |

---

## Historial de Cambios

### [2026-02-11] Migración Backend Python Completa
- ✅ Migración de lógica N8N a Python (FastAPI) en Railway.
- ✅ Endpoints RESTful para validación, testimonios y siniestros.
- ✅ Solución de problemas de dependencias (Pydantic v1 vs Python 3.13).
- ✅ Mejora de algoritmo de testimonios (Mix inteligente y fallback).

### [2026-02-12] Corrección Parseo Pólizas y Siniestros
- ✅ **Backend:** Corrección de lógica de parseo de `ETIQUETA_POLIZA` para soportar múltiples pólizas y estados (ANULADA/VENCE).
- ✅ **Frontend:** Visualización completa de detalles de póliza (Vida, Auxilio, Estado) en el saludo.
- ✅ **Backend:** Endpoint `validate-siniestro` ahora retorna `record_id` de la póliza vinculada.
- ✅ **Frontend:** Formulario Airtable de Siniestros se pre-llena correctamente usando Linked Record ID.

### [2026-03-09] Resolución Carga de Imágenes de Siniestros e ImgBB
- ✅ **Backend:** Integración directa con API de ImgBB para bypass de limitación de Airtable con uploads.
- ✅ **Backend:** Arreglo del bug de formato de adjuntos en Airtable (ahora empaquetando URLs como `[{"url": "..."}]`).
- ✅ **Backend:** El mensaje de éxito del Siniestro ahora expone correctamente el `ID_UNICO_GESTION` generado por la fórmula de Airtable.
- ✅ **Frontend (Linktree):** Añadido botón interactivo en el modal final para Descargar/Compartir el ticket comprobante de la denuncia. 
- 🟢 **Estado actual:** Siniestros funcionando End-to-End en Producción (Railway v9 + Surge).

### [2026-03-10] Rediseño Global: Glassmorphism Premium Compacto
- ✅ **UI/UX:** Despliegue global del diseño "Glassmorphism Premium" en los 8 modales del Linktree.
- ✅ **Optimización:** Reducción agresiva de dimensiones (headers -30%, inputs/botones compactos) para una estética más profesional y equilibrada.
- ✅ **Interactividad:** Resolución de problemas de scroll (`max-height`, `overflow-y`) e interactividad con controles de video YouTube (`backdrop-filter` moderado).
- ✅ **Variantes:** Implementación de variantes temáticas (`danger`, `account`, `employee`) dentro del sistema glassmorphism.
- ✅ **Pulido Final:** Corrección de paletas de color en modales específicos (Ajuste a tonos lilas en "Acceso Autorizado"), ocultamiento de scrollbars nativos y prevención de saltos de línea (text wrapping) en los enlaces del Portal de Autogestión.
- ✅ **Enlaces Actualizados:** Redireccionamiento correcto del enlace de registro de la app al nuevo Portal SaaS (`portal-cliente-seguros.surge.sh/crear-clave.html`).
- 🟢 **Estado actual:** Interfaz 100% premium y funcional desplegada en [seguros-app-linktree.surge.sh](https://seguros-app-linktree.surge.sh/) y [portal-cliente-seguros.surge.sh](https://portal-cliente-seguros.surge.sh/).

### [2026-03-10] Rediseño Portal Cliente: Listas Glassmorphism & Flujos
- ✅ **UI/UX Portal:** Migración de diseño de tarjetas (Grid) a listas (List View) para `Gestiones Generales`, `Accidentes`, `Robo OC` y `Robo/Incendio`. 
- ✅ **Interactividad Portal:** Implementación de Modales globales de detalle (`glass-modal`) al hacer clic en ítems de las listas, permitiendo visualizar información ampliada de manera limpia.
- ✅ **Gestión Documental:** Función de Descarga Integrada. Ahora los usuarios pueden descargar PDFs directamente de la tarjeta de `Pólizas` (leyendo el campo `DOCUMENTACION` de Airtable).
- ✅ **Accesos Rápidos (Quick Actions):** Integración de botones de acción rápida en el header del portal (Denunciar Siniestro, Contactar por WhatsApp, Agente IA).
- ✅ **Integración Linktree:** El botón `Denunciar Siniestro` en el portal redirecciona al Linktree inyectando un parámetro URL (`?modal=siniestro`) para forzar la auto-apertura del modal correspondiente.
- 🟢 **Estado actual:** Funcionalidades de experiencia de usuario premium unificadas en la plataforma SaaS.

*Última actualización: 2026-03-10 21:45*
