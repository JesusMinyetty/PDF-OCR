from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('', views.document_list, name='document_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)