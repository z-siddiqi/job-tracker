from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView

from .models import Task
from .forms import TaskForm

from boards.models import Job
from utils.mixins import JobPermissionMixin, FormInvalidStatus400Mixin


class TaskCreateView(LoginRequiredMixin, JobPermissionMixin, FormInvalidStatus400Mixin, CreateView):
    http_method_names = ["post"]
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"

    # need to override this JobPermissionMixin method since url wont include job slug param
    def get_job(self):
        job_slug = self.request.POST.get("job-slug")
        return get_object_or_404(Job, slug=job_slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = self.get_job()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.job = self.get_job()
        self.object = form.save()
        return TemplateResponse(self.request, "tasks/task.html", {"task": self.object})
