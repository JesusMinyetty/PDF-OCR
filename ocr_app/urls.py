from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('', views.document_list, name='document_list'),
    path('document/<int:pk>/status/', views.document_status, name='document_status'),
    path('status/bulk/', views.documents_status_bulk, name='documents_status_bulk'),
]
