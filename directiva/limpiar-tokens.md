# POE: Limpiar Tokens Expirados

## Objetivo
Eliminar registros de tokens expirados o usados de la tabla Airtable para mantener rendimiento

## Entradas
- Base Airtable: `appuhslj3GFf60Tea`
- Tabla: `Tokens`
- Token API: (desde .env)

## Herramientas
- Script: `ejecucion/limpiar_tokens.py`

## Pasos
1. Consultar todos los tokens de la tabla
2. Filtrar tokens donde USADO = true O EXPIRA < ahora
3. Eliminar registros filtrados
4. Reportar cantidad eliminada

## Salidas
- Tokens expirados eliminados
- Log de cantidad eliminada

## Casos Límite
- Si hay más de 100 tokens: usar paginación
- Rate limit de Airtable: 5 requests/segundo
- Si falla: reintentar con backoff exponencial

## Frecuencia
- Semanal o cuando tabla > 1000 registros

## Tiempo Estimado
- 1-2 minutos para 500 registros
