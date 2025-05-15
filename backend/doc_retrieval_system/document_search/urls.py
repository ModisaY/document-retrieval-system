from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('document/<int:doc_id>/', views.document_view, name='document_view'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/upload/', views.upload_document, name='upload_document'),
    path('api/rebuild-index/', views.rebuild_index, name='rebuild_index'),
]