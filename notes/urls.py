from django.urls import path

from .views import NoteUpdateView

urlpatterns = [
    path('<int:app_pk>/', NoteUpdateView.as_view(), name='note_update'),
]
