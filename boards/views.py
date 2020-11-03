from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, UpdateView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Board, Job
from .forms import BoardForm
from .mixins import CustomLoginRequiredMixin


def ajax_required(f):

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return redirect('home')
        return f(request, *args, **kwargs)
    
    return wrap


def custom_handler404(request, exception):
    return render(request, '404.html', status=404)


def custom_handler500(request):
    return render(request, '500.html', status=500)


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


class ApplicationCreateView(CustomLoginRequiredMixin, CreateView):
    model = Job
    template_name = 'application_new.html'
    fields = (
        'board', 
        'company', 
        'title', 
        'url', 
        'deadline', 
        'progress', 
        'notes'
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicationUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'application_detail.html'
    pk_url_kwarg = 'app_pk'
    context_object_name = 'application'
    fields = (
        'board', 
        'company', 
        'title', 
        'url', 
        'deadline', 
        'progress', 
        'notes'
    )

    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    def handle_no_permission(self):
        return redirect('home')


class ApplicationDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs['app_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    def handle_no_permission(self):
        return redirect('home')
    
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
        print('Deleted.')
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


class BoardUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, pk=self.kwargs['board_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def handle_no_permission(self):
        return redirect('home')
    
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


class BoardDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, View):
    
    def get_object(self):
        return get_object_or_404(Board, pk=self.kwargs['board_pk'])
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
    def handle_no_permission(self):
        return redirect('home')
    
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
