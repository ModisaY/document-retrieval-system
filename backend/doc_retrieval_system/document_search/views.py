from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from .utils import search_documents, build_inverted_index, process_text
import json
import time

def index(request):
    """Render the search interface"""
    return render(request, 'document_search/index.html')

def document_view(request, doc_id):
    """Render a document preview page"""
    try:
        document = Document.objects.get(id=doc_id)
        return render(request, 'document_search/document.html', {'document': document})
    except Document.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

@csrf_exempt
@require_POST
def upload_document(request):
    """API endpoint to add a new document"""
    try:
        data = json.loads(request.body)
        
        if not data.get('content'):
            return JsonResponse({'error': 'Document content is required'}, status=400)
        
        # Create document
        doc = Document.objects.create(
            title=data.get('title', 'Untitled'),
            content=data['content']
        )
        
        # Update index for this document only
        build_inverted_index(document_id=doc.id)
        
        return JsonResponse({
            'status': 'success', 
            'id': doc.id,
            'title': doc.title
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def search_api(request):
    query = request.GET.get('q', '')
    limit = int(request.GET.get('limit', 10))

    if not query.strip():
        return JsonResponse({'results': []})

    start_time = time.time()  # ⏱ Start measuring
    results = search_documents(query, limit)
    end_time = time.time()    # ⏱ End measuring

    search_duration = end_time - start_time
    print(f"Search time for '{query}': {search_duration:.4f} seconds")  # Log to console

    response = {
        'query': query,
        'query_terms': process_text(query),
        'count': len(results),
        'search_time_seconds': round(search_duration, 4),  # You can also return to frontend if you want
        'results': results
    }

    return JsonResponse(response)

@csrf_exempt
@require_POST
def rebuild_index(request):
    """API endpoint to rebuild the entire index"""
    try:
        build_inverted_index()
        return JsonResponse({'status': 'success', 'message': 'Index rebuilt successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)