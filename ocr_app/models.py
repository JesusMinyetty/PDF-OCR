from django.db import models

class PDFDocument(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Subido'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]
    
    original_pdf = models.FileField(upload_to='pdfs/')
    ocr_pdf = models.FileField(upload_to='ocr_pdfs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    ocr_text = models.FileField(upload_to='ocr_text/', blank=True, null=True)