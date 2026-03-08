---
# TESTS INTEGRALES (PREPARACIÓN DE SCRIPT)

## Objetivo
- Validar el flujo completo: envío de datos, adjuntos, edge cases y feedback.

## Estructura del script (pytest)

```python
import requests

def test_envio_siniestro():
    url = 'https://web-production-2584d.up.railway.app/api/create-siniestro'
    datos = {
        'tipo_formulario': 'choque',
        'poliza_record_id': 'recXXXXXXXXXXXXXX',
        'dni': '20015207',
        'datos': '{"nombre": "Test User", "descripcion": "Test de envío"}',
    }
    files = {'foto_dano': open('test_dano.jpg', 'rb')}
    resp = requests.post(url, data=datos, files=files)
    assert resp.status_code == 200
    res = resp.json()
    assert res['status'] == 'success' or res['status'] == 'warning'


def test_edge_cases():
    # Campos vacíos
    ...
    # Demasiados adjuntos
    ...
```

## Notas
- El script debe ubicarse en `/ejecucion/main_test.py`.
- Se usa pytest y requests.
- Los tests cubren todos los estados posibles según feedback.

---
