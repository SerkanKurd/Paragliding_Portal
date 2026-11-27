FROM python:3.14-slim-trixie

# UV_COMPILE_BYTECODE: bağımlılıklar build sırasında derlenir, çalışırken .venv'e yazılmaz.
# UV_NO_SYNC: çalışırken 'uv run' ortamı senkronlamaya (paket kurmaya) çalışmaz.
# PATH: 'python' ve 'gunicorn' doğrudan .venv'den çalışır.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_SYNC=1 \
    UV_CACHE_DIR=/tmp/uv-cache \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && rm -rf /var/lib/apt/lists/*

# uv kurulumu (sürüm sabit; CI'daki sürümle aynı)
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /bin/

# Önce bağımlılıkları kopyala ve kur (geliştirme araçları, ör. ruff, imaja girmez)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

# Projenin tamamını kopyala (CI'da derlenen CSS'ler de gelir)
COPY . .

# Nginx için statikleri topla
# collectstatic settings'i yükler; build sırasında gerçek anahtar gerekmez.
# Bu değer yalnızca bu RUN adımında geçerlidir, imajın ortamına girmez.
RUN SECRET_KEY=collectstatic-build-only python manage.py collectstatic --no-input

# Yetkisiz kullanıcı. Statik/medya klasörleri ona ait olur; yeni oluşturulan
# Docker volume'ları bu sahipliği imajdan devralır.
RUN useradd --system --uid 10001 --create-home --home-dir /home/app app \
    && mkdir -p /app/mediafiles \
    && chown -R app:app /app/staticfiles /app/mediafiles \
    && chmod +x /app/docker-entrypoint.sh

USER app

EXPOSE 8000

# Açılışta statik dosyaları volume'a kopyalar, sonra verilen komutu çalıştırır.
# docker-compose'daki 'command' da bu entrypoint üzerinden çalışır.
ENTRYPOINT ["/app/docker-entrypoint.sh"]
# Gunicorn ayarları gunicorn.conf.py'den okunur
CMD ["gunicorn", "core.wsgi:application"]
