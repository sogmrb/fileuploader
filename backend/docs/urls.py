from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('signed-url/<int:doc_id>/', views.GetSignedUrlView.as_view(), name='get-signed-url'),
    path('documents/', views.DocumentListView.as_view(), name='document-list'),
    path('documents/<int:doc_id>/ask/', views.QuestionAnswerView.as_view(), name='ask-question'),
    path('documents/<int:doc_id>/', views.DeleteDocumentView.as_view(), name='delete-document'),
]
