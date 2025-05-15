from django.urls import path
from . import views

# Define URL patterns for document search app
urlpatterns = [
    path('search/', views.search_api, name='search_api'),  # Search endpoint
    path('upload/', views.upload_document, name='upload_document'),  # Upload endpoint
    path('rebuild-index/', views.rebuild_index, name='rebuild_index'),  # Rebuild index endpoint
    path('document/<int:doc_id>/', views.get_document_api, name='get_document_api'),  # Get document by ID
]