# SISTEMA DE SEGUROS AGÉNTICOS

Sistema de gestión inteligente para Rafael Allende & Asociados Seguros.

## Estructura del Proyecto

```
SISTEMA-DE-SEGUROS-AGENTICOS/
├── SaaS-Login/           # Portal de autenticación y acceso
│   ├── index.html        # Página de login
│   ├── welcome.html      # Página de bienvenida post-login
│   ├── registro.html     # Registro de nuevos usuarios
│   └── workflows/        # Definiciones de n8n
│       ├── LOGIN SISTEMA-AGENTICO.json
│       ├── PORTAL SISTEMA-AGENTICO.json
│       ├── REGISTRO SISTEMA-AGENTICO.json
│       └── REDIRECT SISTEMA-AGENTICO.json
└── README.md
```

## Componentes

### 1. SaaS-Login
Portal de autenticación con:
- Login con validación contra Airtable
- Registro de nuevos usuarios
- Sistema de tokens temporales para URLs enmascaradas
- Soporte multi-rol (GERENTE, EMPLEADO, etc.)

## URLs de Producción

| Componente | URL |
|------------|-----|
| Login | https://login-agentico-1770227340.surge.sh |
| Registro | https://registro-agentico-1770227370.surge.sh |
| n8n Backend | https://primary-production-0abcf.up.railway.app |

## Tecnologías

- **Frontend:** HTML/CSS/JS (Vanilla)
- **Backend:** n8n (Railway)
- **Base de Datos:** Airtable
- **Hosting:** Surge.sh

## Fecha de Creación
2026-02-04
