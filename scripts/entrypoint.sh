#!/bin/sh
set -eu
cd /app/backend
python -m alembic upgrade head
exec gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout 60 \
  --graceful-timeout 30 \
  --keep-alive 5 \
  --access-logfile - \
  --error-logfile - \
  --forwarded-allow-ips="*"
