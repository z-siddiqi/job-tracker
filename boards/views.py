from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

from .models import Board, Job
from .forms import BoardForm, JobForm
from .serializers import BoardSerializer, JobSerializer
from .scrape import get_job_info

from tasks.forms import TaskForm
from utils.mixins import ajax_required, BoardPermissionMixin, JobPermissionMixin, FormInvalidStatus400Mixin


@ajax_required
@login_required
def scrape_job(request, board_slug):
    if request.method == "GET":
        url = request.GET.get("jobUrl")
        data = get_job_info(url)
        return JsonResponse(data)


class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"

    def get_queryset(self):
        objs = self.model.objects
        return objs.filter(user=self.request.user)


class BoardCreateView(LoginRequiredMixin, FormInvalidStatus400Mixin, CreateView):
    model = Board
    form_class = BoardForm
    template_name = "boards/board_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)


class BoardDetailView(LoginRequiredMixin, BoardPermissionMixin, DetailView):
    model = Board
    slug_url_kwarg = "board_slug"
    template_name = "boards/board_detail.html"
    redirect_url = "board_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columns"] = ("applied", "phone", "onsite", "offer")
        job_serializer = JobSerializer(self.object.jobs, many=True)
        context["jobs"] = job_serializer.data
        return context


class BoardUpdateView(LoginRequiredMixin, BoardPermissionMixin, FormInvalidStatus400Mixin, UpdateView):
    model = Board
    slug_url_kwarg = "board_slug"
    form_class = BoardForm
    template_name = "boards/board_update.html"

    def form_valid(self, form):
        self.object = form.save()
        board_serializer = BoardSerializer(instance=self.object)
        return JsonResponse({"board": board_serializer.data})


class BoardDeleteView(LoginRequiredMixin, BoardPermissionMixin, DeleteView):
    model = Board
    slug_url_kwarg = "board_slug"
    form_class = BoardForm
    template_name = "boards/board_delete.html"

    def get_success_url(self):
        return reverse("board_list")


class JobCreateView(LoginRequiredMixin, BoardPermissionMixin, FormInvalidStatus400Mixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "boards/job_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.get_board()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.board = self.get_board()
        self.object = form.save()
        job_serializer = JobSerializer(instance=self.object)
        return JsonResponse({"job": job_serializer.data})


class JobUpdateView(LoginRequiredMixin, JobPermissionMixin, FormInvalidStatus400Mixin, UpdateView):
    model = Job
    slug_url_kwarg = "job_slug"
    form_class = JobForm
    template_name = "boards/job_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.tasks.all()
        context["task_form"] = TaskForm()
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        job_serializer = JobSerializer(instance=self.object)
        return JsonResponse({"job": job_serializer.data})


class JobDeleteView(LoginRequiredMixin, JobPermissionMixin, DeleteView):
    model = Job
    slug_url_kwarg = "job_slug"
    template_name = "boards/job_delete.html"

    def form_valid(self, form):
        self.object.delete()
        return HttpResponse(status=204)
