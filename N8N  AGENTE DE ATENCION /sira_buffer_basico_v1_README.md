# Buffer básico importable para n8n

Este flujo usa solo nodos base:
- Webhook
- Set
- Wait
- Code
- Respond to Webhook

## Qué hace
No agrega múltiples mensajes todavía.
Hace una pausa de 5 segundos antes de responder, para que el agente no conteste instantáneamente.

## Para probar
Mandá un POST al webhook con:

```json
{
  "chatId": "demo-1",
  "message": "Hola, soy Diego López"
}
```

## Salida
Devuelve:
- `message_compiled`
- `raw_messages`
- `message_count`
- `buffer_applied`

## Próximo paso
Cuando confirmes que este importa bien, seguimos con el buffer real con Redis.
