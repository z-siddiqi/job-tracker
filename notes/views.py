from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, View
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Note
from.forms import NoteForm

from boards.models import Job
from utils.mixins import ajax_required, CustomLoginRequiredMixin, CustomUserPassesTestMixin


class NoteUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_job(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])

    def get_object(self):
        job = self.get_job()
        return Note.objects.get(job=job)
    
    def test_func(self):
        obj = self.get_object()
        return obj.job.board.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        job = self.get_job()
        note = self.get_object()
        form = NoteForm(instance=note)
        context = {'job': job, 'note': note, 'form': form}
        data['html'] = render_to_string(
            'app/note_update.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        note = self.get_object()
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
