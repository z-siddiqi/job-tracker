from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Board, Job

# Create your views here.
@login_required
def board_detail(request, pk):
    applications = Job.objects.filter(board=pk).order_by('deadline')
    board = Board.objects.get(id=pk)
    columns = (
        'Applied',
        'Phone',
        'Onsite',
        'Offer',
    )
    context = {'applications': applications, 'board': board, 'columns': columns}
    return render(request, 'board_detail.html', context)
    
class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'application_detail.html'
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

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'application_delete.html'
    context_object_name = 'application'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.board.user == self.request.user

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

class BoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Board
    template_name = 'board_delete.html'
    context_object_name = 'board'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

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
