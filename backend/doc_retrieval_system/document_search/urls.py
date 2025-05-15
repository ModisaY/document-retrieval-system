from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_api, name='search_api'),
    path('upload/', views.upload_document, name='upload_document'),
    path('rebuild-index/', views.rebuild_index, name='rebuild_index'),
    path('document/<int:doc_id>/', views.get_document_api, name='get_document_api'),  # ✅ Added
]