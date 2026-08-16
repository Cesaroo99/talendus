FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_ENV=production \
    DEBUG=false \
    PORT=8000 \
    STORAGE_DIR=/var/data \
    WEB_CONCURRENCY=2

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin talendus \
    && mkdir -p /var/data /app

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/backend/requirements.txt

COPY --chown=talendus:talendus backend /app/backend
COPY --chown=talendus:talendus scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY --chown=talendus:talendus admin /app/admin
COPY --chown=talendus:talendus assets /app/assets
COPY --chown=talendus:talendus en /app/en
COPY --chown=talendus:talendus *.html robots.txt sitemap.xml /app/

RUN chmod +x /app/scripts/entrypoint.sh \
    && chown -R talendus:talendus /var/data /app

USER talendus
EXPOSE 8000
WORKDIR /app/backend
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
