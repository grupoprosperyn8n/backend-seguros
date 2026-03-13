# SIRA SUPREMA v10.3 — Importable n8n

## Qué incluye
- Webhook de entrada
- Inyección de prompts y variables
- Preparación de contexto
- Guardrails
- Sentimiento
- Infracciones
- Agente con memoria Redis y modelo OpenAI
- Respuesta por webhook
- Placeholders deshabilitados para tools

## Antes de usar
1. Importá el JSON en tu instancia.
2. Asigná credenciales de OpenAI y Redis.
3. Revisá el nodo Memoria Redis y poné tu conexión real.
4. Si querés herramientas reales, activá y configurá los 4 nodos placeholder.
5. Probalo primero con payload mínimo:

```json
{
  "chatId": "demo-1",
  "message": "Hola, soy Diego López y quiero consultar mi póliza"
}
```

## Importante
Este flujo está optimizado para importar bien en una instancia n8n parecida a la tuya, usando los mismos tipos de nodos que mostraste.
La parte de tools queda preparada como placeholder porque el backend exacto depende de tus endpoints y autenticación.
