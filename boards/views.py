from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, UpdateView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Board, Job
from .forms import BoardForm
from .scrape import scrape_indeed_posting

from utils.mixins import ajax_required, CustomLoginRequiredMixin, CustomUserPassesTestMixin


@ajax_required
@login_required
def scrape_job(request, board_pk):
    if request.method == 'POST':
        url = request.POST.get('jobUrl')
        data = scrape_indeed_posting(url)
        return JsonResponse(data)
    else:
        redirect_url = reverse('application_new', kwargs={'board_pk': board_pk})
        return redirect(redirect_url)


@login_required
def board_detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    applications = Job.objects.filter(board=board)
    if board.user == request.user:
        columns = (
            'Applied',
            'Phone',
            'Onsite',
            'Offer',
        )
        context = {'applications': applications, 'board': board, 'columns': columns}
        return render(request, 'board_detail.html', context)
    else:
        return redirect('home')


class ApplicationCreateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, CreateView):
    model = Job
    template_name = 'application_new.html'
    fields = (
        'company', 
        'title', 
        'deadline', 
        'progress', 
        'description'
    )

    def get_object(self):
        return get_object_or_404(Board, pk=self.kwargs['board_pk'])
        
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def get_context_data(self):
        context = super().get_context_data()
        context["board"] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.board = self.get_object()
        return super().form_valid(form)


class ApplicationUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'application_detail.html'
    pk_url_kwarg = 'app_pk'
    context_object_name = 'application'
    fields = (
        'company', 
        'title', 
        'deadline', 
        'progress', 
        'description'
    )

    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user


class ApplicationDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs['app_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        application = self.get_object()
        context = {'application': application}
        data['html_form'] = render_to_string(
            'application_delete.html', 
            context=context, 
            request=request
        )
        return JsonResponse(data)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = dict()
        application = self.get_object()
        application.delete()
        data['form_is_valid'] = True
        data['redirect_url'] = reverse('board_detail', kwargs={'board_pk': kwargs['board_pk']})
        return JsonResponse(data)


class BoardCreateView(CustomLoginRequiredMixin, View):
    
    @method_decorator(ajax_required)
    def get(self, request):
        data = dict()
        form = BoardForm()
        context = {'form': form}
        data['html_form'] = render_to_string(
            'board_new.html', 
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
            data['redirect_url'] = reverse('board_detail', kwargs={'board_pk': new_board.pk})
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class BoardUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, pk=self.kwargs['board_pk'])
    
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
            'board_update.html', 
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
            data['redirect_url'] = reverse('board_detail', kwargs={'board_pk': kwargs['board_pk']})
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class BoardDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, pk=self.kwargs['board_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        data = dict()
        board = self.get_object()
        context = {'board': board}
        data['html_form'] = render_to_string(
            'board_delete.html', 
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
        data['redirect_url'] = reverse('home')
        return JsonResponse(data)
