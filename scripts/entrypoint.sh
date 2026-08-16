#!/bin/sh
set -eu
cd /app/backend
mkdir -p "${STORAGE_DIR:-/var/data}"

echo "Talendus: attente de PostgreSQL..."
python - <<'PY'
import os
import sys
import time

from sqlalchemy import create_engine, text

from app.boot import normalize_database_url

url = normalize_database_url(os.environ.get("DATABASE_URL", ""))
if not url or url.startswith("sqlite"):
    print("DATABASE_URL PostgreSQL manquant.", file=sys.stderr)
    sys.exit(1)

last = None
for attempt in range(1, 31):
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("PostgreSQL prêt.")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001 — attente de la base au boot
        last = exc
        print(f"Attente PostgreSQL ({attempt}/30) : {exc}")
        time.sleep(2)
print(f"PostgreSQL inaccessible : {last}", file=sys.stderr)
sys.exit(1)
PY

echo "Talendus: migrations..."
if ! python -m alembic upgrade head; then
  echo "Talendus: migration en échec, nouvel essai..." >&2
  sleep 3
  python -m alembic upgrade head || echo "Talendus: migration toujours en échec — démarrage du site public quand même." >&2
fi
echo "Talendus: démarrage HTTP..."
exec gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-1}" \
  --timeout 120 \
  --graceful-timeout 20 \
  --keep-alive 5 \
  --max-requests 400 \
  --max-requests-jitter 50 \
  --worker-tmp-dir /tmp \
  --access-logfile - \
  --error-logfile - \
  --forwarded-allow-ips="*"
