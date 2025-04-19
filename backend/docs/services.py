import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import PyPDF2
import io
import json
import random
from .models import UploadedDocument

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

def generate_signed_url(file_key, expires_in=3600):
    s3_client = get_s3_client()
    try:
        return s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=expires_in
        )
    except ClientError as e:
        raise Exception(f"Failed to generate signed URL: {str(e)}")

def process_pdf_file(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        page_count = len(pdf_reader.pages)
        
        text_metadata = {}
        full_text = ""
        
        for page_num in range(page_count):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            full_text += text
            
            text_metadata[page_num] = {
                'start_pos': len(full_text) - len(text),
                'end_pos': len(full_text)
            }
        
        return {
            'page_count': page_count,
            'text_metadata': text_metadata,
            'extracted_text': full_text
        }
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")

def get_random_text_segment(doc):
    if not doc.text_metadata:
        raise Exception('Document text not processed')
    
    page_num = random.randint(0, doc.page_count - 1)
    page_metadata = doc.text_metadata[str(page_num)]
    
    start_pos = page_metadata['start_pos']
    end_pos = page_metadata['end_pos']
    page_text = doc.extracted_text[start_pos:end_pos]
    
    segments = [s.strip() for s in page_text.split('.') if s.strip()]
    if not segments:
        raise Exception('No text segments found')
    
    segment = random.choice(segments)
    segment_start = page_text.find(segment)
    segment_end = segment_start + len(segment)
    
    return {
        'page': page_num,
        'text': segment,
        'start_pos': start_pos + segment_start,
        'end_pos': start_pos + segment_end
    } 