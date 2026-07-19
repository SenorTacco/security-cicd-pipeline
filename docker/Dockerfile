# ---- Base Image ----
FROM python:3.14-slim AS base

# Guvenlik: root olmayan kullanici olustur
RUN groupadd -r appuser && useradd -r -g appuser appuser

# /api/ping endpoint'i icin ping komutu (slim imajda yuklu gelmez)
RUN apt-get update && \
    apt-get install -y --no-install-recommends iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Calisma dizini
WORKDIR /app

# Bagimliliklari once kopyala (Docker cache optimizasyonu)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala (secure versiyonu)
COPY app/secure/ .

# Kalici veritabani icin veri dizini (volume mount noktasi)
RUN mkdir -p /app/data && chown appuser:appuser /app/data

# Guvenlik: root olmayan kullaniciya gec
USER appuser

# Docker icinde 0.0.0.0'a bind etmek gerekli
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
# Veritabani volume uzerinde tutulur; konteyner silinse de veri kalir
ENV DATABASE_PATH=/app/data/app.db

# Port ac
EXPOSE 5000

# Saglik kontrolu
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Uygulamayi baslat
CMD ["python", "app.py"]
