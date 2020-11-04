from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Task
from .forms import TaskForm

from utils.mixins import ajax_required, CustomLoginRequiredMixin, CustomUserPassesTestMixin


class TaskListView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        tasks = Task.objects.filter(user=request.user)
        context={'form': form, 'tasks': tasks}
        return render(request, 'task_list.html', context)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task = form.save()
            data['task'] = model_to_dict(new_task)
            return JsonResponse(data)
        else:
            return redirect('task_list')


class TaskCompleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['task_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        return redirect('task_list')

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        task = Task.objects.get(pk=self.kwargs['task_pk'])
        task.completed = True
        task.save()
        data['task'] = model_to_dict(task)
        return JsonResponse(data)


class TaskDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['task_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        return redirect('task_list')
    
    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        task = Task.objects.get(pk=kwargs['task_pk'])
        task.delete()
        data['result'] = 'ok'
        return JsonResponse(data)
