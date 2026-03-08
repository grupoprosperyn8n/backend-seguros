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

*Última actualización: 2026-02-12 12:00*
