# ocr_app/tasks.py
import os
import logging
import subprocess
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
import ocrmypdf
import pdfplumber
from docx import Document
from django.conf import settings
from ocrmypdf.exceptions import TaggedPDFError, PriorOcrFoundError
from .models import PDFDocument

logger = logging.getLogger(__name__)

def create_word_document(text_content, output_path):
    """Crea un documento Word a partir del texto extraído."""
    try:
        doc = Document()
        
        # Configurar estilos básicos
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = 12
        
        # Agregar contenido
        for index, text in enumerate(text_content):
            # Agregar texto de la página
            doc.add_paragraph(text)
            
            # Agregar separador de página (excepto en la última página)
            if index < len(text_content) - 1:
                doc.add_paragraph().add_run().add_break()
        
        # Guardar documento
        doc.save(output_path)
        return True
    except Exception as e:
        logger.error(f"Error creando DOCX: {str(e)}")
        return False

@shared_task(
    bind=True,
    autoretry_for=(TaggedPDFError,),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True
)
def process_pdf_task(self, pdf_id):
    pdf_doc = PDFDocument.objects.get(id=pdf_id)
    input_path = pdf_doc.original_pdf.path
    output_path = f"{input_path}_ocr.pdf"
    clean_path = f"{input_path}_clean.pdf"
    docx_path = None

    try:
        # Limpieza inicial del PDF
        try:
            subprocess.run(
                ["pdftk", input_path, "output", clean_path, "drop_xfa", "dont_ask"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            input_file = clean_path
        except Exception as e:
            logger.warning(f"Error limpiando PDF: {str(e)}")
            input_file = input_path

        # Procesamiento OCR principal
                # Procesamiento OCR principal
        ocrmypdf.ocr(
            input_file,
            output_path,
            language="spa+eng",
            force_ocr=True,
            optimize=1,
            progress_bar=False
        )

        # Extraer texto para DOCX
        text_content = []
        try:
            with pdfplumber.open(output_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
        except Exception as e:
            logger.error(f"Error extrayendo texto: {str(e)}")
            raise

        # Generar documento Word si hay texto
        if text_content:
            docx_filename = f"{os.path.splitext(os.path.basename(output_path))[0]}.docx"
            docx_fullpath = os.path.join(settings.MEDIA_ROOT, 'ocr_text', docx_filename)
            
            os.makedirs(os.path.dirname(docx_fullpath), exist_ok=True)
            
            if create_word_document(text_content, docx_fullpath):
                pdf_doc.ocr_text.name = os.path.join('ocr_text', docx_filename)
                logger.info(f"DOCX generado: {docx_fullpath}")
            else:
                logger.warning("No se pudo generar el DOCX")

        # Actualizar estado del documento
        pdf_doc.ocr_pdf.name = os.path.relpath(output_path, start=os.path.join(os.getcwd(), 'media'))
        pdf_doc.status = 'completed'
        pdf_doc.save()

    except TaggedPDFError as e:
        logger.warning(f"Reintento {self.request.retries} para PDF {pdf_id}")
        raise self.retry(exc=e)
    
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}", exc_info=True)
        pdf_doc.status = 'failed'
        pdf_doc.message = str(e)[:255]
        pdf_doc.save()
        raise
    
    finally:
        # Limpieza de archivos temporales
        try:
            if os.path.exists(clean_path):
                os.remove(clean_path)
        except Exception as e:
            logger.error(f"Error limpiando archivos temporales: {str(e)}")

    return {
        'pdf_id': pdf_id,
        'ocr_pdf': pdf_doc.ocr_pdf.url if pdf_doc.ocr_pdf else None,
        'ocr_text': pdf_doc.ocr_text.url if pdf_doc.ocr_text else None
    }