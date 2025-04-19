from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import UploadedDocument, QuestionAnswer
from .serializers import UploadedDocumentSerializer, QuestionAnswerSerializer
from .services import (
    generate_signed_url,
    process_pdf_file,
    get_random_text_segment
)
from django.core.files.base import ContentFile
import os

class UploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UploadedDocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the file name without extension
            file_name = os.path.splitext(request.data['file'].name)[0]
            
            # Create the document with the file name as title
            doc = serializer.save(title=file_name)
            
            pdf_data = process_pdf_file(doc.file)
            doc.page_count = pdf_data['page_count']
            doc.text_metadata = pdf_data['text_metadata']
            doc.extracted_text = pdf_data['extracted_text']
            doc.processed = True
            doc.save()
            
            # Generate signed URL
            signed_url = generate_signed_url(doc.file.name)
            
            response_data = UploadedDocumentSerializer(doc).data
            response_data['file_url'] = signed_url
            return Response(response_data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetSignedUrlView(APIView):
    def get(self, request, doc_id):
        try:
            doc = UploadedDocument.objects.get(id=doc_id)
            signed_url = generate_signed_url(doc.file.name)
            return Response({'signed_url': signed_url})
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentListView(APIView):
    def get(self, request):
        documents = UploadedDocument.objects.all().order_by('-uploaded_at')
        serializer = UploadedDocumentSerializer(documents, many=True)
        return Response(serializer.data)

class QuestionAnswerView(APIView):
    def post(self, request, doc_id):
        try:
            doc = UploadedDocument.objects.get(id=doc_id)
            question = request.data.get('question')
            
            if not question:
                return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get random text segment
            reference = get_random_text_segment(doc)
            
            # Create Q&A
            qa = QuestionAnswer.objects.create(
                document=doc,
                question=question,
                answer=f"Here's a relevant text from page {reference['page'] + 1}: {reference['text']}",
                references=[reference]
            )
            
            serializer = QuestionAnswerSerializer(qa)
            return Response(serializer.data)
            
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteDocumentView(APIView):
    def delete(self, request, doc_id):
        try:
            doc = UploadedDocument.objects.get(id=doc_id)
            doc.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
