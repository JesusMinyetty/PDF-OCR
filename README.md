# PDF OCR Processor (Django + Celery)

Aplicación web desarrollada en Django para la gestión, digitalización (OCR) y extracción de texto de documentos PDF, exportándolos a formato Word (.docx).

## 🛠️ Stack Tecnológico
- **Backend:** Django 5.x
- **Procesamiento Asíncrono:** Celery + Redis
- **Motor OCR:** `ocrmypdf` (Tesseract-OCR)
- **Extracción de Texto:** `pdfplumber`
- **Generación de Word:** `python-docx`

## ⚙️ Requisitos del Sistema (Instalación Previa)
Antes de instalar las librerías de Python, tu sistema operativo debe tener instaladas las siguientes herramientas a nivel de SO:

1. **Tesseract-OCR** (Motor de reconocimiento óptico)
   - Ubuntu/Debian: `sudo apt install tesseract-ocr tesseract-ocr-spa ghostscript`
   - macOS: `brew install tesseract tesseract-lang ghostscript`
   - Windows: Descargar instalador desde [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
2. **Redis** (Message Broker para Celery)
   - Ubuntu/Debian: `sudo apt install redis-server`
   - macOS: `brew install redis`
3. **pdftk** (Herramienta de limpieza de PDFs)
   - Ubuntu: `sudo apt install pdftk`

## 🚀 Instalación y Ejecución

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone https://github.com/JesusMinyetty/PDF.git
   cd PDF