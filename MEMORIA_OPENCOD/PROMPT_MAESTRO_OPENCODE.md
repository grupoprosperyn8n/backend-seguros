# 🚀 INICIALIZACIÓN DE CONTEXTO - SISTEMA DE SEGUROS AGÉNTICOS
> **Instrucción para el Agente (OpenCode / Antigravity):**
> Lee cuidadosamente este documento y ejecuta los pasos en orden ANTES de responder a cualquier solicitud del usuario o escribir código.

---

## 🛑 PASO 1: CARGA DE MEMORIA PRINCIPAL
Tu primer objetivo es entender de qué trata este proyecto, qué arquitectura tiene y en qué estado se dejó la última vez.
**TU ACCIÓN REQUERIDA:** 
Utiliza la herramienta `view_file` para leer completamente el siguiente archivo:
👉 `/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/MEMORIA_OPENCOD/MEMORIA.md`

*(Nota mental: Ahí encontrarás que el Frontend está en Surge, el Backend Python en Railway, y la Base de Datos es Airtable).*

---

## 🛑 PASO 2: COMPRENSIÓN DE BUGS RESUELTOS
No debes volver a cometer errores del pasado (especialmente con la carga de archivos, ImgBB y el formateo estricto de URLs que exige Airtable).
**TU ACCIÓN REQUERIDA:**
Utiliza la herramienta `view_file` para leer el registro de problemas resueltos:
👉 `/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/MEMORIA_OPENCOD/FICHA_TECNICA_PROBLEMA.md`

---

## 🛑 PASO 3: CARGA DE CREDENCIALES Y ENTORNO
Para hacer tu trabajo, vas a necesitar conectarte a Airtable, Github, Railway y servidores MCP. 
**TU ACCIÓN REQUERIDA:**
Utiliza la herramienta `view_file` para leer y cargar en tu contexto todas las variables de entorno necesarias desde este archivo confidencial:
👉 `/home/diegol/Descargas/Antigravity/HABILIDADES DE AGENTES/SISTEMA-DE-SEGUROS-AGENTICOS/DOCUMENTACION_DESPLIEGUE.md`

---

## 🛑 PASO 4: REGLAS DE ORO DEL PROYECTO
Antes de ejecutar la petición actual del usuario, asimila estas reglas inquebrantables:

1. **NO ROMPER LO QUE FUNCIONA:** El Flujo de Siniestros (Backend v9 python -> ImgBB -> Airtable) funciona PERFECTO. No modifiques la lógica central si no se te pide explícitamente.
2. **DETERMINISMO:** La lógica de negocio pesada va en el Backend de Python (FastAPI).
3. **DESPLIEGUES:** Todo cambio en `main.py` requiere pushear a GitHub (`master`) y hacer redeploy en Railway. Todo cambio en el frontend Linktree (`app.js`, `index.html`) requiere comando `surge`.
4. **SERVIDORES MCP DISPONIBLES:** En esta instancia posees conexión vía MCP a GitHub, Perplexity (Ask), y n8n/Supabase. Úsalos sabiamente.

---

## ✅ CONFIRMACIÓN
Una vez que hayas leído los 3 archivos indicados y asimilado las reglas, responde ÚNICAMENTE con el siguiente mensaje:
**"🟢 Contexto de Rafael Allende & Asociados cargado exitosamente. Sistemas comprendidos, credenciales mapeadas. ¿Qué construimos hoy, Diego?"**
