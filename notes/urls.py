from django.urls import path

from .views import NoteUpdateView

urlpatterns = [
    path('<str:job_slug>/', NoteUpdateView.as_view(), name='note_update'),
]
