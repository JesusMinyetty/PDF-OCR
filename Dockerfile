FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalación de dependencias del sistema para OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    ghostscript \
    unpaper \
    && (apt-get install -y --no-install-recommends pdftk || apt-get install -y --no-install-recommends pdftk-java || true) \
    && rm -rf /var/lib/apt/lists/*

# Instalación de dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear carpetas necesarias
RUN mkdir -p /app/media /app/data

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
