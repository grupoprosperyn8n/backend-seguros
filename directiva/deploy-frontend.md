# POE: Deploy Frontend a Producción

## Objetivo

Desplegar cambios del frontend del Sistema de Seguros a Surge.sh

## Entradas

- Carpeta: `SaaS-Login/`
- Dominio: `login-agentico-1770227340.surge.sh`

## Herramientas

- Script: `ejecucion/deploy_surge.py`
  - Login: `python3 deploy_surge.py`
  - Linktree: `python3 deploy_surge.py --linktree`
- Comando directo: `npx surge`

## Pasos

1. Verificar que no hay errores en el código
2. Ejecutar deploy con Surge
3. Confirmar mensaje "Success!"
4. Probar URL en navegador
5. Actualizar MEMORIA.md

## Salidas

- Frontend actualizado en producción
- Registro en MEMORIA.md

## Casos Límite

- Si Surge falla por autenticación: `npx surge login`
- Si hay errores 404: verificar que index.html existe
- Si CSS no carga: verificar rutas relativas

## Tiempo Estimado

- 2-3 minutos
