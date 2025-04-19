from rest_framework import serializers
from .models import UploadedDocument, QuestionAnswer

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['id', 'title', 'file', 'page_count', 'processed', 'uploaded_at']
        read_only_fields = ['page_count', 'processed', 'uploaded_at']
        extra_kwargs = {
            'title': {'required': False}
        }

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'answer', 'references', 'created_at']
        read_only_fields = ['answer', 'references', 'created_at'] 