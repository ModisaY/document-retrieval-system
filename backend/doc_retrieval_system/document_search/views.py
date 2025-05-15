from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import time
from .models import Document
from .utils import search_documents, build_inverted_index, process_text

# Swagger schema for upload document
upload_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["content"],
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Optional document title"),
        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Text content of the document"),
    },
)

# Upload Document API
@swagger_auto_schema(method='post', request_body=upload_schema, operation_description="Upload a new document.")
@api_view(['POST'])
@csrf_exempt
def upload_document(request):
    try:
        data = json.loads(request.body)

        if not data.get('content'):
            return Response({'error': 'Document content is required'}, status=400)

        doc = Document.objects.create(
            title=data.get('title', 'Untitled'),
            content=data['content']
        )

        build_inverted_index(document_id=doc.id)

        return Response({
            'status': 'success',
            'id': doc.id,
            'title': doc.title
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# Swagger parameters for search
search_parameters = [
    openapi.Parameter('q', openapi.IN_QUERY, description="Search keyword", type=openapi.TYPE_STRING),
    openapi.Parameter('limit', openapi.IN_QUERY, description="Limit number of results", type=openapi.TYPE_INTEGER),
]

# Search Documents API
@swagger_auto_schema(method='get', manual_parameters=search_parameters, operation_description="Search documents by keyword.")
@api_view(['GET'])
def search_api(request):
    query = request.GET.get('q', '')
    limit = int(request.GET.get('limit', 10))

    if not query.strip():
        return Response({'results': []})

    start_time = time.time()
    results = search_documents(query, limit)
    end_time = time.time()

    search_duration = end_time - start_time
    print(f"Search Query: {query} | Time taken: {search_duration:.4f} seconds")

    response = {
        'query': query,
        'query_terms': process_text(query),
        'count': len(results),
        'search_time_seconds': round(search_duration, 4),
        'results': results
    }

    return Response(response)

# Rebuild Inverted Index API
@swagger_auto_schema(method='post', operation_description="Rebuild the inverted index from all documents.")
@api_view(['POST'])
@csrf_exempt
def rebuild_index(request):
    try:
        build_inverted_index()
        return Response({'status': 'success', 'message': 'Index rebuilt successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# Full Document Preview API
@swagger_auto_schema(method='get', operation_description="Retrieve full document details by document ID.")
@api_view(['GET'])
@require_GET
def get_document_api(request, doc_id):
    try:
        document = Document.objects.get(id=doc_id)
        return Response({
            'id': document.id,
            'title': document.title,
            'content': document.content,
            'created_at': document.created_at,
        })
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=404)

# Simple Index View for Testing
def index(request):
    return JsonResponse({"message": "Backend running. Use /swagger/ for API documentation."})
