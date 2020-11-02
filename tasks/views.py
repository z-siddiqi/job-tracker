from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Task
from .forms import TaskForm

# Create your views here.
class TaskList(View):
    def get(self, request):
        form = TaskForm()
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'task_list.html', context={'form': form, 'tasks': tasks})

    def post(self, request):
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
