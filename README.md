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


## Frontend Components

### DocumentList
Displays a list of uploaded documents with metadata and actions.

### PDFViewer
Renders PDF documents with navigation and text highlighting capabilities.

### ChatInterface
Provides an interactive Q&A interface for documents.

### FileUploader
Handles document uploads with progress tracking.
