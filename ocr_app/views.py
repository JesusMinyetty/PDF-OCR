import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import PDFDocument
from .forms import PDFDocumentForm
from .tasks import process_pdf_task

logger = logging.getLogger(__name__)

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_doc = form.save()
            # Delegamos TODO el trabajo a Celery. 
            # No procesamos OCR aquí para no bloquear el servidor web.
            process_pdf_task.delay(pdf_doc.id)
            return redirect('document_detail', pk=pdf_doc.pk)
    else:
        form = PDFDocumentForm()
        
    return render(request, 'upload.html', {'form': form})

def document_detail(request, pk):
    document = get_object_or_404(PDFDocument, pk=pk)
    return render(request, 'detail.html', {'document': document})

def document_list(request):
    document_list = PDFDocument.objects.all().order_by('-created_at')
    paginator = Paginator(document_list, 10) # 10 documentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'document_list.html', {'page_obj': page_obj})

def document_status(request, pk):
    """Endpoint JSON para consultar el estado de un documento en tiempo real (AJAX)."""
    document = get_object_or_404(PDFDocument, pk=pk)
    return JsonResponse({
        'id': document.id,
        'status': document.status,
        'status_display': document.get_status_display(),
        'message': document.message or '',
        'ocr_pdf_url': document.ocr_pdf.url if document.ocr_pdf else None,
        'ocr_text_url': document.ocr_text.url if document.ocr_text else None,
    })


def documents_status_bulk(request):
    """Endpoint JSON para consultar el estado de varios documentos a la vez (para la lista)."""
    ids = request.GET.get('ids', '')
    id_list = [int(i) for i in ids.split(',') if i.strip().isdigit()]
    docs = PDFDocument.objects.filter(id__in=id_list).values('id', 'status')
    return JsonResponse({'documents': list(docs)})