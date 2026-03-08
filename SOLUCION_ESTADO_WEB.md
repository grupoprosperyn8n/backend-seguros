# 🔧 SOLUCIÓN: Campo ESTADO_WEB con Single Select

## 📊 **FORMATO EXACTO EN AIRTABLE**

Verificado por API en las 3 tablas de denuncias:

```python
Opción 1: "🆕 NUEVO WEB"     # Emoji + Espacio + Texto
Opción 2: "👀 VISTO"         # Emoji + Espacio + Texto
Opción 3: "✅ PROCESADO"     # Emoji + Espacio + Texto
```

**Nota:** Aunque visualmente pueda verse sin espacio, el valor almacenado en Airtable SÍ contiene espacio (U+0020) después del emoji.

---

## ✅ **SOLUCIÓN IMPLEMENTADA**

### **1. Crear Clase de Constantes**

Agregar al inicio de `backend/main.py` (después de los imports, antes de las funciones):

```python
# ==============================================================================
# CONSTANTES DE ESTADO WEB
# ==============================================================================

class EstadoWeb:
    """
    Valores exactos para el campo ESTADO_WEB en tablas de denuncias.

    IMPORTANTE: Estos valores DEBEN coincidir EXACTAMENTE con las opciones
    configuradas en Airtable (Single Select). Cualquier diferencia (espacios,
    mayúsculas, emojis) causará que el campo quede NULL.

    Verificado en:
    - DENUNCIA DE ACCIDENTE
    - DENUNCIA ROBO OC
    - DENUNCIA ROBO / INCENDIO
    """
    NUEVO_WEB = "🆕 NUEVO WEB"
    VISTO = "👀 VISTO"
    PROCESADO = "✅ PROCESADO"
```

### **2. Actualizar Línea 981**

**ANTES (incorrecto):**
```python
airtable_payload["ESTADO_WEB"] = "NUEVO WEB"
```

**DESPUÉS (correcto):**
```python
airtable_payload["ESTADO_WEB"] = EstadoWeb.NUEVO_WEB
```

---

## 🎯 **VENTAJAS DE ESTA SOLUCIÓN**

### ✅ **Centralizado**
- Un solo lugar para cambiar si Airtable se modifica
- Fácil de mantener

### ✅ **Type-Safe**
- IDEs ofrecen autocompletado
- Reduce errores de tipeo

### ✅ **Documentado**
- La clase tiene docstring explicando la importancia
- Futuras modificaciones saben qué hacer

### ✅ **Flexible**
Si necesitas cambiar el formato:
```python
# Solo cambiar aquí:
class EstadoWeb:
    NUEVO_WEB = "🆕NUEVO WEB"  # Sin espacio si fuera necesario
    # O incluso leer dinámicamente del API...
```

---

## 📝 **CÓDIGO COMPLETO PARA IMPLEMENTAR**

```python
# ==============================================================================
# CONSTANTES DE ESTADO WEB
# ==============================================================================

class EstadoWeb:
    """
    Valores exactos para el campo ESTADO_WEB en tablas de denuncias.

    IMPORTANTE: Estos valores DEBEN coincidir EXACTAMENTE con las opciones
    configuradas en Airtable (Single Select). Cualquier diferencia causará
    que el campo quede NULL debido a las restricciones de Single Select.

    Single Select requiere:
    - Match exacto (case-sensitive)
    - Emojis exactos
    - Espacios exactos
    - Sin variaciones

    Tablas afectadas:
    - DENUNCIA DE ACCIDENTE
    - DENUNCIA ROBO OC
    - DENUNCIA ROBO / INCENDIO

    Verificado: 2026-03-03 via Airtable Meta API
    """
    NUEVO_WEB = "🆕 NUEVO WEB"
    VISTO = "👀 VISTO"
    PROCESADO = "✅ PROCESADO"


# ==============================================================================
# ENDPOINT: Crear Siniestro
# ==============================================================================

@app.post("/api/create-siniestro")
async def create_siniestro(request: Request):
    """
    ... (resto del código) ...
    """

    # ... (líneas 841-980) ...

    # ==================================================================
    # 6. AGREGAR CAMPOS AUTOMÁTICOS
    # ==================================================================

    # Estado web (CORREGIDO - ahora usa valor exacto de Single Select)
    airtable_payload["ESTADO_WEB"] = EstadoWeb.NUEVO_WEB

    print(f"   📦 Payload Airtable keys: {list(airtable_payload.keys())}")

    # ... (resto del código) ...
```

---

## 🧪 **TESTING**

### **Test 1: Verificar que el valor coincide**
```python
# Agregar al final de main.py (solo para testing):
if __name__ == "__main__":
    print("Testing EstadoWeb constantes:")
    print(f"NUEVO_WEB: '{EstadoWeb.NUEVO_WEB}'")
    print(f"Bytes: {EstadoWeb.NUEVO_WEB.encode('utf-8')}")
    print(f"Length: {len(EstadoWeb.NUEVO_WEB)}")
```

### **Test 2: Crear denuncia y verificar**
1. Crear denuncia desde frontend
2. Verificar en Airtable que ESTADO_WEB = "🆕 NUEVO WEB"
3. Debería verse con el emoji

---

## 🔄 **SI NECESITAS CAMBIAR EL FORMATO**

Si después de implementar descubres que necesitas otro formato:

### **Opción A: Leer dinámicamente del API**
```python
import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def get_estado_web_values():
    """Lee valores válidos directamente de Airtable"""
    meta_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(meta_url, headers=headers)

    tables = response.json().get("tables", [])
    for table in tables:
        if table["name"] == "DENUNCIA DE ACCIDENTE":
            for field in table.get("fields", []):
                if field["name"] == "ESTADO_WEB":
                    choices = field.get("options", {}).get("choices", [])
                    return {
                        "NUEVO_WEB": choices[0]["name"],
                        "VISTO": choices[1]["name"],
                        "PROCESADO": choices[2]["name"],
                    }
    return None

# Uso:
valores = get_estado_web_values()
airtable_payload["ESTADO_WEB"] = valores["NUEVO_WEB"]
```

### **Opción B: Variable de entorno**
```python
# .env
ESTADO_WEB_NUEVO=🆕 NUEVO WEB
ESTADO_WEB_VISTO=👀 VISTO
ESTADO_WEB_PROCESADO=✅ PROCESADO

# backend/main.py
class EstadoWeb:
    NUEVO_WEB = os.getenv("ESTADO_WEB_NUEVO", "🆕 NUEVO WEB")
    VISTO = os.getenv("ESTADO_WEB_VISTO", "👀 VISTO")
    PROCESADO = os.getenv("ESTADO_WEB_PROCESADO", "✅ PROCESADO")
```

---

## ✅ **CHECKLIST DE IMPLEMENTACIÓN**

- [ ] Agregar clase `EstadoWeb` al inicio de `backend/main.py`
- [ ] Cambiar línea 981: usar `EstadoWeb.NUEVO_WEB`
- [ ] Hacer commit: "fix: usar valor exacto para Single Select ESTADO_WEB"
- [ ] Deploy a Railway
- [ ] Crear denuncia de prueba desde frontend
- [ ] Verificar en Airtable que ESTADO_WEB se llena correctamente
- [ ] Confirmar que 100% de nuevas denuncias tienen estado

---

## 📈 **IMPACTO ESPERADO**

### **ANTES:**
- ❌ 98% de denuncias con ESTADO_WEB vacío
- ❌ Imposible filtrar denuncias web
- ❌ Pérdida de trazabilidad

### **DESPUÉS:**
- ✅ 100% de denuncias con ESTADO_WEB correcto
- ✅ Filtrado funcional en Airtable
- ✅ Trazabilidad completa de origen web

---

## 🔍 **CÓMO VERIFICAR EL FIX**

```bash
# 1. Hacer el cambio
cd backend
# editar main.py

# 2. Commit
git add main.py
git commit -m "fix: usar valor exacto Single Select ESTADO_WEB"

# 3. Deploy
git push origin main

# 4. Verificar
# - Ir al linktree
# - Crear denuncia de prueba
# - Ver en Airtable si ESTADO_WEB = "🆕 NUEVO WEB"
```
