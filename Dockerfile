FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SCRIPTS_DIR=/app/scripts
ENV REPORTS_DIR=/app/data/reports
ENV TRANSLATION_ENABLED=0
ENV PORT=5050

EXPOSE 5050

CMD gunicorn frontend.wsgi:app \
    --bind 0.0.0.0:5050 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
