FROM python:3.12-slim

# Evita arquivos .pyc e habilita output imediato de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Coleta arquivos estáticos para o WhiteNoise servir em produção
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Gunicorn como servidor WSGI de produção
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py criar_superuser && gunicorn portal_cooperativa.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]