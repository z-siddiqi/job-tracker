from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

from .models import Task
from .forms import TaskForm

from utils.mixins import ajax_required, JobPermissionMixin, TaskPermissionMixin
from utils.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView


class TaskCreateView(LoginRequiredMixin, JobPermissionMixin, AjaxCreateView):
    http_method_names = ["post"]
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.job = self.get_job()
        return super().form_valid(form)

    def get_success_data(self):
        return {"status": 200, "task": model_to_dict(self.object)}


class TaskCompleteView(LoginRequiredMixin, TaskPermissionMixin, AjaxUpdateView):
    http_method_names = ["post"]
    model = Task
    pk_url_kwarg = "task_pk"

    def update(self, request, *args, **kwargs):
        self.object.completed = not self.object.completed  # toggle the boolean field
        self.object.save()
        self.response_payload = self.get_success_data()
        return self.render_to_response({})

    def get_success_data(self):
        return {"status": 200}

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.update(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, TaskPermissionMixin, AjaxDeleteView):
    http_method_names = ["post"]
    model = Task
    pk_url_kwarg = "task_pk"

    def get_success_data(self):
        return {"status": 200}
