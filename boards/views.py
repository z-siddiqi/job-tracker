from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from .models import Board, Job
from .forms import BoardForm, JobForm
from .scrape import get_job_info

from notes.models import Note
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
        return render(request, 'app/board_detail.html', context)
    else:
        return redirect('home')


class BoardListView(CustomLoginRequiredMixin, ListView):
    model = Board
    template_name = 'app/board_list.html'
    context_object_name = 'boards'

    def get_queryset(self):
        objs = self.model.objects
        return objs.filter(user=self.request.user)


class BoardCreateView(CustomLoginRequiredMixin, View):
    
    @method_decorator(ajax_required)
    def get(self, request):
        data = dict()
        form = BoardForm()
        context = {'form': form}
        data['html_form'] = render_to_string(
            'app/board_create.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request):
        data = dict()
        form = BoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            new_board.user = request.user
            new_board = form.save()
            data['form_is_valid'] = True
            data['redirect_url'] = reverse('board_detail', kwargs={'board_slug': new_board.slug})
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
        data['html_form'] = render_to_string(
            'app/board_update.html', 
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
            data['redirect_url'] = reverse('board_detail', kwargs={'board_slug': kwargs['board_slug']})
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class BoardDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, slug=self.kwargs['board_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        context = {'board': board}
        data['html_form'] = render_to_string(
            'app/board_delete.html', 
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
        data['redirect_url'] = reverse('board_list')
        return JsonResponse(data)


class JobCreateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, CreateView):
    model = Job
    template_name = 'app/job_create.html'
    fields = (
        'company', 
        'title', 
        'deadline', 
        'progress', 
        'description'
    )

    def get_board(self):
        return get_object_or_404(Board, slug=self.kwargs['board_slug'])
        
    def test_func(self):
        obj = self.get_board()
        return obj.user == self.request.user
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["board"] = self.get_board()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.board = self.get_board()
        self.object = form.save()
        Note.objects.create(job=self.object)
        return HttpResponseRedirect(self.get_success_url())


class JobDetailView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, TemplateView):
    template_name = 'app/job_detail.html'

    def get_object(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["job"] = self.get_object()
        return context


class JobUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        job = self.get_object()
        form = JobForm(instance=job)
        context = {'job': job, 'form': form}
        data['html'] = render_to_string(
            'app/job_update.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

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
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        job = self.get_object()
        context = {'job': job}
        data['html_form'] = render_to_string(
            'app/job_delete.html', 
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
        data['redirect_url'] = reverse('board_detail', kwargs={'board_slug': kwargs['board_slug']})
        return JsonResponse(data)
