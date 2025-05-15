from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class InvertedIndex(models.Model):
    term = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='index_entries')
    frequency = models.IntegerField()
    tf_idf = models.FloatField(default=0.0)
    
    class Meta:
        # Composite unique constraint to allow same term in different documents
        unique_together = ('term', 'document')
        indexes = [
            models.Index(fields=['term']),  # Speed up term-based lookups
        ]
    
    def __str__(self):
        return f"{self.term} in {self.document.title}"
