from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Task
from .forms import TaskForm

from boards.models import Job
from utils.mixins import JobPermissionMixin
from utils.views import AjaxCreateView


class TaskCreateView(LoginRequiredMixin, JobPermissionMixin, AjaxCreateView):
    http_method_names = ["post"]
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"

    # need to override this JobPermissionMixin method since url wont include job slug param
    def get_job(self):
        job_slug = self.request.POST.get("job-slug")
        return get_object_or_404(Job, slug=job_slug)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.job = self.get_job()
        return super().form_valid(form)

    def get_success_data(self):
        return {
            "status": 200,
            "task_html": render_to_string(
                template_name="tasks/task.html",
                context={"task": self.object},
                request=self.request,
            ),
        }
