# Memoria del Proyecto SaaS-Login

Este archivo registra los cambios críticos, versiones estables y soluciones a problemas recurrentes específicos de este módulo (Login, Registro, Portal).

## [2026-02-04 16:30] Estabilización de Flujos y "Blindaje" Airtable

### Estado: ✅ ESTABLE (Producción)

### Cambios Críticos Realizados
1.  **Blindaje de Nodos Airtable (Explicit Column Mapping):**
    *   **Problema:** Error recurrente `column "role" does not exist` debido a que n8n buscaba columnas eliminadas en Airtable.
    *   **Solución:** Se editó el JSON de los nodos (Login, Portal, Registro) para solicitar **explícitamente** solo las columnas `EMAIL`, `ROL OPERATIVO`, `ESTADO`, `URL_PORTAL`, etc.
    *   **Regla de Oro:** Si agregas una columna nueva en Airtable, debes agregarla manualmente a la lista `fields` en el nodo de n8n.

2.  **Lógica de Portal Mejorada:**
    *   Soporte para columna `ROL` tipo Multi-select (Arrays).
    *   Match estricto con `ROL OPERATIVO` (mayúsculas) del usuario.

3.  **Renombramiento de Archivos:**
    *   `LOGIN SISTEMA-AGENTICO.json`
    *   `PORTAL SISTEMA-AGENTICO.json`
    *   `REGISTRO SISTEMA-AGENTICO.json`

4.  **URLs de Producción (Surge):**
    *   **Login:** `https://login-agentico-1770227340.surge.sh`
    *   **Registro:** `https://registro-agentico-1770227370.surge.sh` (Corregido para apuntar al form de registro y redirigir al login).

### Versiones de Nodos
*   **Airtable Node:** Version 2 (Estable). **NO ACTUALIZAR A 2.1** (Rompe la configuración).

### Cómo recuperar el sistema si falla
1.  Borrar los nodos actuales en n8n.
2.  Importar los archivos JSON locales (asegurar que sean los "SISTEMA-AGENTICO").
3.  Reconectar credenciales y activar.

### Auditoría de Seguridad (2026-02-04)
*   **Login:** Bloquea credenciales inválidas y no permite enumeración de usuarios.
*   **XSS:** Frontend protegido contra inyección de scripts básicos.
*   **Registro:** Validación correcta de correos duplicados.
*   **Conclusión:** Sistema seguro para uso en producción.
