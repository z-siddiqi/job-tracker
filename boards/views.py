from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, ListView
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from .models import Board, Job
from .forms import BoardForm, JobForm
from .scrape import get_job_info

from notes.models import Note
from notes.forms import NoteForm
from tasks.models import Task
from tasks.forms import TaskForm
from utils.mixins import ajax_required, CustomLoginRequiredMixin, CustomUserPassesTestMixin


@ajax_required
@login_required
def scrape_job(request, board_slug):
    if request.method == 'POST':
        url = request.POST.get('jobUrl')
        data = get_job_info(url)
        return JsonResponse(data)
    else:
        redirect_url = reverse('job_create', kwargs={'board_slug': board_slug})
        return redirect(redirect_url)


@login_required
def board_detail(request, board_slug):
    board = get_object_or_404(Board, slug=board_slug)
    jobs = Job.objects.filter(board=board)
    if board.user == request.user:
        columns = (
            'Applied',
            'Phone',
            'Onsite',
            'Offer',
        )
        context = {'jobs': jobs, 'board': board, 'columns': columns}
        return render(request, 'boards/board_detail.html', context)
    else:
        return redirect('home')


class BoardListView(CustomLoginRequiredMixin, ListView):
    model = Board
    template_name = 'boards/board_list.html'
    context_object_name = 'boards'

    def get_queryset(self):
        objs = self.model.objects
        return objs.filter(user=self.request.user)


class BoardCreateView(CustomLoginRequiredMixin, View):
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        form = BoardForm()
        context = {'form': form}
        data['html'] = render_to_string(
            'boards/board_create.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        form = BoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            new_board.user = request.user
            new_board = form.save()
            data['form_is_valid'] = True
            data['redirect_url'] = new_board.get_absolute_url()
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class BoardUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, slug=self.kwargs['board_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        form = BoardForm(instance=board)
        context = {'board': board, 'form': form}
        data['html'] = render_to_string(
            'boards/board_update.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['redirect_url'] = board.get_absolute_url()
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class BoardDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, slug=self.kwargs['board_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def get_success_url(self):
        return reverse('board_list')

    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        context = {'board': board}
        data['html'] = render_to_string(
            'boards/board_delete.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        board.delete()
        data['form_is_valid'] = True
        data['redirect_url'] = self.get_success_url()
        return JsonResponse(data)


class JobCreateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):

    def get_board(self):
        return get_object_or_404(Board, slug=self.kwargs['board_slug'])
        
    def test_func(self):
        obj = self.get_board()
        return obj.user == self.request.user

    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        board = self.get_board()
        form = JobForm()
        context = {'board': board, 'form': form}
        data['html'] = render_to_string(
            'boards/job_create.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.user = request.user
            new_job.board = self.get_board()
            new_job = form.save()
            Note.objects.create(job=new_job)
            data['form_is_valid'] = True
            data['redirect_url'] = new_job.get_absolute_url()
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class JobDetailView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    template_name = 'boards/job_detail.html'

    def get_object(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def get_note(self):
        return Note.objects.get(job=self.job) 

    def get_tasks(self):
        return Task.objects.filter(job=self.job)
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user

    def get_context_data(self, **kwargs):
        # job
        kwargs['job'] = self.job
        kwargs['job_form'] = JobForm(instance=self.job)

        # tasks
        tasks = self.get_tasks()
        kwargs['tasks'] = tasks
        kwargs['task_form'] = TaskForm()

        # note
        note = self.get_note()
        kwargs['note'] = note
        kwargs['note_form'] = NoteForm(instance=note)

        return kwargs
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        self.job = self.get_object()
        data = dict()
        data['html'] = render_to_string(
            template_name=self.template_name, 
            context=self.get_context_data(),
            request=request
        )
        return JsonResponse(data)


class JobUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        job = self.get_object()
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class JobDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user

    def get_success_url(self):
        return reverse('board_detail', kwargs={'board_slug': self.kwargs['board_slug']})
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        job = self.get_object()
        context = {'job': job}
        data['html'] = render_to_string(
            'boards/job_delete.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        job = self.get_object()
        job.delete()
        data['form_is_valid'] = True
        data['redirect_url'] = self.get_success_url()
        return JsonResponse(data)
