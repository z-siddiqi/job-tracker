from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from .models import Task
from .forms import TaskForm

from boards.models import Job
from utils.mixins import ajax_required, CustomLoginRequiredMixin, CustomUserPassesTestMixin


class TaskListView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_job(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def test_func(self):
        obj = self.get_job()
        return obj.board.user == self.request.user

    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        form = TaskForm()
        job = self.get_job()
        tasks = Task.objects.filter(job=job)
        context={'job': job, 'tasks': tasks, 'form': form}
        data['html'] = render_to_string(
            'app/task_list.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        form = TaskForm(request.POST)
        job = self.get_job()
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.job = job
            new_task = form.save()
            data['task'] = model_to_dict(new_task)
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class TaskCompleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['task_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.job.board.user == self.request.user

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        task = Task.objects.get(pk=self.kwargs['task_pk'])
        if not task.completed:
            task.completed = True
        else:
            task.completed = False
        task.save()
        data['task'] = model_to_dict(task)
        return JsonResponse(data)


class TaskDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['task_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.job.board.user == self.request.user
    
    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        task = Task.objects.get(pk=kwargs['task_pk'])
        task.delete()
        data['result'] = 'ok'
        return JsonResponse(data)
