from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from .models import Note

from boards.models import Job
from utils.mixins import CustomLoginRequiredMixin, CustomUserPassesTestMixin


class NoteUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'app/note_update.html'
    fields = ('note', )

    def get_application(self):
        return get_object_or_404(Job, pk=self.kwargs['app_pk'])

    def get_object(self):
        job = self.get_application()
        return Note.objects.get(job=job)

    def test_func(self):
        obj = self.get_object()
        return obj.job.board.user == self.request.user
    
    def get_context_data(self):
        context = super().get_context_data()
        context["application"] = self.get_application()
        return context
