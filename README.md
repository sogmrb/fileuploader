# Leagle File Uploader

A web application for uploading, viewing, and interacting with PDF documents. Built with Django (backend) and Next.js (frontend).

## Features

- PDF document upload and storage
- Document list view with metadata
- PDF viewer with text highlighting
- Interactive Q&A interface
- AWS S3 integration for file storage
- Real-time document processing

## Tech Stack

### Backend
- Django
- Django REST Framework
- PyPDF2 for PDF processing
- AWS S3 for file storage
- SQLite (development) / PostgreSQL (production)

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- React PDF Viewer
- Axios for API calls

## Backend Architecture

### Models

#### UploadedDocument
- `title`: Document title (derived from file name)
- `file`: PDF file stored in AWS S3
- `page_count`: Number of pages in the document
- `processed`: Boolean indicating if document has been processed
- `uploaded_at`: Timestamp of upload
- `extracted_text`: Full text content of the document
- `text_metadata`: JSON field storing text positions and page mappings

#### QuestionAnswer
- `document`: Foreign key to UploadedDocument
- `question`: User's question
- `answer`: Generated answer with references
- `references`: JSON array of text references with page numbers and positions
- `created_at`: Timestamp of Q&A creation

### Views

#### UploadView
- Handles PDF file uploads
- Extracts file name for document title
- Processes PDF to extract text and metadata
- Generates signed S3 URLs for file access

#### DocumentListView
- Lists all uploaded documents
- Returns document metadata and processing status

#### QuestionAnswerView
- Processes user questions
- Generates answers with text references
- Returns structured Q&A data

#### GetSignedUrlView
- Generates temporary signed URLs for S3 file access
- Used for secure document viewing

### PDF Processing

The application uses PyPDF2 to:
- Extract text content from PDFs
- Calculate page counts
- Generate text metadata including:
  - Page numbers
  - Text positions
  - Character offsets
- Support reference tracking

## Frontend Components

### DocumentList
Displays a list of uploaded documents with metadata and actions.

### PDFViewer
Renders PDF documents with navigation and text highlighting capabilities.

### ChatInterface
Provides an interactive Q&A interface for documents.

### FileUploader
Handles document uploads with progress tracking.

## Setup Instructions

### Backend Setup
1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

### Frontend Setup
1. Install dependencies: `npm install`
2. Start the development server: `npm run dev`

## API Endpoints

- `POST /upload/`: Upload a PDF document
- `GET /documents/`: List all documents
- `GET /signed-url/<doc_id>/`: Get signed URL for document
- `POST /documents/<doc_id>/ask/`: Ask a question about a document
- `DELETE /documents/<doc_id>/`: Delete a document
