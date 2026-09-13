from django import forms
from .models import PDFDocument
from django.core.exceptions import ValidationError

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['original_pdf']
        
        
def clean_original_pdf(self):
        file = self.cleaned_data['original_pdf']
        # Validar extensión
        if not file.name.lower().endswith('.pdf'):
            raise ValidationError("Solo se permiten archivos PDF.")
        # Validar tamaño (ej: 50MB)
        max_size = 100 * 1024 * 1024
        if file.size > max_size:
            raise ValidationError("El archivo no puede superar los 100MB.")
        return file        