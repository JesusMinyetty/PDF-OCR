from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView # <-- NUEVO
from django.conf import settings
from django.conf.urls.static import static
from ocr_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='document_list', permanent=False)), # <-- NUEVO
    
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('list/', views.document_list, name='document_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)