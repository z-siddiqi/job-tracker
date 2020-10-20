from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Board, Job

def custom_handler404(request, exception):
    return render(request, '404.html', status=404)


def custom_handler500(request):
    return render(request, '500.html', status=500)


@login_required
def board_detail(request, board_pk):
    applications = Job.objects.filter(board=board_pk).order_by('deadline')
    board = Board.objects.get(id=board_pk)
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


class ApplicationCreateView(LoginRequiredMixin, CreateView):
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
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user
    
    def handle_no_permission(self):
        return redirect('home')


@login_required
def application_delete(request, board_pk, app_pk):
    data = dict()
    application = get_object_or_404(Job, pk=app_pk)
    if application.board.user == request.user:
        if request.method == 'POST':
            application.delete()
            data['form_is_valid'] = True
            data['redirect_url'] = reverse('board_detail', kwargs={'board_pk': board_pk})
        else:
            context = {'application': application}
            data['html_form'] = render_to_string('application_delete.html', context=context, request=request)
        return JsonResponse(data)
    else:
        return redirect('home')


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    template_name = 'board_new.html'
    fields = (
        'title', 
    )
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def board_delete(request, board_pk):
    data = dict()
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            board.delete()
            data['form_is_valid'] = True
            data['redirect_url'] = reverse('home')
        else:
            context = {'board': board}
            data['html_form'] = render_to_string('board_delete.html', context=context, request=request)
        return JsonResponse(data)
    else:
        return redirect('home')
