from django.contrib import admin
from .models import UploadedDocument, QuestionAnswer

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_count', 'processed', 'uploaded_at')
    list_filter = ('processed', 'uploaded_at')
    search_fields = ('title', 'extracted_text')
    readonly_fields = ('page_count', 'processed', 'uploaded_at', 'extracted_text', 'text_metadata')

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('document', 'question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question', 'answer', 'document__title')
    readonly_fields = ('created_at',)
