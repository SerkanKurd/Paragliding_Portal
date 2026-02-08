FROM python:3.14-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && rm -rf /var/lib/apt/lists/*

# uv kurulumu
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Önce bağımlılıkları kopyala ve kur
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Projenin tamamını kopyala (Zaten yerelde derlediğin CSS'ler de gelecek)
COPY . .

# Nginx için statikleri topla
RUN uv run python manage.py collectstatic --no-input

CMD ["uv", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]