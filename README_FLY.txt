CHIMBITA-FLY-FIXED-INTEGRATED-CRON
==================================

Bot Telegram que escanea los pares USDT perpetuals de Binance. Se ejecuta una vez y termina (cron puro).
Preparado para Fly.io con Dockerfile (python:3.11-slim).

Despliegue en Fly.io
--------------------
1) Instalar CLI:
   curl -L https://fly.io/install.sh | sh

2) Login:
   fly auth signup   # o  fly auth login

3) Crear app (si no existe) en región Santiago (scl), sin desplegar aún:
   fly launch --name chimbita-fly-fixed --region scl --no-deploy

4) Desplegar imagen:
   fly deploy

Prueba manual
-------------
   fly ssh console -C "python scan_bot.py"

Mensajes esperados en Telegram:
   🔵 Bot CHIMBITA-FLY-FIXED-INTEGRATED started on Fly.io
   Scan completed — analyzed N USDT perpetual pairs. No aligned signals found.
   (o un aviso con exchangeInfo_error.json si Binance bloquea la región)

Programar ejecución cada hora
-----------------------------
Usa Fly Machines con schedule cron (si tu plan lo soporta). Ejemplo genérico:

   # Crea una máquina con cron "cada hora" que ejecute el script y salga
   fly machines create --app chimbita-fly-fixed --region scl      --schedule "0 * * * *"      --image $(fly platform status --json | jq -r '.platform.dockerImage' 2>/dev/null || echo "")      --command "python scan_bot.py"

Actualizar
----------
   fly deploy -a chimbita-fly-fixed

Eliminar app
------------
   fly apps destroy chimbita-fly-fixed
