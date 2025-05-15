import spacy
import math
from collections import defaultdict
from django.core.cache import cache
from .models import Document, InvertedIndex

# Load spaCy model for NLP processing
nlp = spacy.load("en_core_web_sm")

def process_text(text):
    """Process text to extract meaningful tokens (lemmatized, no stopwords)"""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return tokens

def calculate_document_length(doc_content):
    """Calculate document length (number of tokens)"""
    tokens = process_text(doc_content)
    return len(tokens)

def build_inverted_index(document_id=None):
    """
    Build or update the inverted index.
    If document_id is provided, only update for that document.
    Otherwise, rebuild the entire index.
    """
    if document_id:
        documents = Document.objects.filter(id=document_id)
        InvertedIndex.objects.filter(document_id=document_id).delete()
    else:
        documents = Document.objects.all()
        InvertedIndex.objects.all().delete()
    
    term_doc_freq = defaultdict(set)  # Track which docs contain each term
    doc_lengths = {}  # Store length of each document
    
    for doc in documents:
        tokens = process_text(doc.content)  # Lemmatized tokens
        doc_lengths[doc.id] = len(tokens)
        
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        
        for term, freq in term_freq.items():
            term_doc_freq[term].add(doc.id)
            InvertedIndex.objects.create(
                term=term,               # Store lemmatized token
                document=doc,
                frequency=freq,
                tf_idf=0.0
            )
    
    total_docs = Document.objects.count()
    
    # Calculate and update TF-IDF for each term-document pair
    for term, doc_ids in term_doc_freq.items():
        df = len(doc_ids)
        idf = math.log(total_docs / (df + 1))
        
        for index_entry in InvertedIndex.objects.filter(term=term):
            doc_id = index_entry.document_id
            tf = index_entry.frequency / max(1, doc_lengths.get(doc_id, 1))
            index_entry.tf_idf = tf * idf
            index_entry.save()
    
    clear_search_cache()

def clear_search_cache():
    """Clear all search-related cache entries"""
    cache_keys = [key for key in cache._cache.keys() if key.startswith('search_')]
    for key in cache_keys:
        cache.delete(key)

def search_documents(query, limit=10):
    """
    Search documents based on query terms.
    Returns ranked results with relevance scores.
    """
    cache_key = f"search_{query}_{limit}"
    cached_results = cache.get(cache_key)
    if cached_results:
        return cached_results
    
    # Process query
    query_tokens = process_text(query)
    if not query_tokens:
        return []
    
    # Score documents based on TF-IDF
    doc_scores = defaultdict(float)
    for token in query_tokens:
        indices = InvertedIndex.objects.filter(term=token)
        for index in indices:
            # Add TF-IDF score for this term to document's total score
            doc_scores[index.document.id] += index.tf_idf
    
    # Rank documents by score and limit results
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    # Get document details for results
    results = []
    for doc_id, score in ranked_docs:
        doc = Document.objects.get(id=doc_id)
        # Find matching terms for highlighting
        highlight_context = get_highlight_context(doc.content, query_tokens)
        
        results.append({
            'id': doc.id,
            'title': doc.title,
            'content_preview': highlight_context,
            'score': round(score, 3),
            'match_terms': list(set(t for t in query_tokens if InvertedIndex.objects.filter(term=t, document_id=doc_id).exists()))
        })
    
    # Cache results for 5 minutes
    cache.set(cache_key, results, 300)
    return results

def get_highlight_context(content, query_terms, context_size=50):
    """Get context around the first query term match for highlighting"""
    content_lower = content.lower()
    for term in query_terms:
        pos = content_lower.find(term)
        if pos >= 0:
            start = max(0, pos - context_size)
            end = min(len(content), pos + len(term) + context_size)
            
            # Adjust to avoid cutting words
            if start > 0:
                while start > 0 and content[start] != ' ':
                    start -= 1
                start += 1  # Move past the space
            
            if end < len(content):
                while end < len(content) and content[end] != ' ':
                    end += 1
            
            context = content[start:end]
            if start > 0:
                context = "..." + context
            if end < len(content):
                context = context + "..."
            
            return context
    
    # If no term is found, return the beginning of the content
    return content[:200] + "..." if len(content) > 200 else content