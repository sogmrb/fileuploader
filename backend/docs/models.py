from django.db import models
from django.utils import timezone

class UploadedDocument(models.Model):
    """
    Represents an uploaded PDF document with its metadata and extracted text.
    """
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='documents/')
    page_count = models.IntegerField(default=0)
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(default=timezone.now)
    extracted_text = models.TextField(blank=True)
    text_metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Uploaded Document'
        verbose_name_plural = 'Uploaded Documents'

    def __str__(self):
        return f"{self.title or 'Untitled'} ({self.page_count} pages)"

class QuestionAnswer(models.Model):
    """
    Represents a question-answer pair for a document with references to the source text.
    """
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    references = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Question Answer'
        verbose_name_plural = 'Question Answers'

    def __str__(self):
        return f"Q&A for {self.document.title} ({self.created_at})"
