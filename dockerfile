# Hafif bir imajla başlıyoruz
FROM python:3.14-slim

# Sistem bağımlılıkları (ARM cihazlarda derleme gerekebilir)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# uv kurulumu (Hızlı paket yönetimi için)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
# --no-cache kullanarak imaj boyutunu küçültüyoruz
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Proje dosyalarını kopyala
COPY . .

# Django static dosyalarını topla
RUN uv run python manage.py collectstatic --no-input

# Uygulamayı başlat
CMD ["uv", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]