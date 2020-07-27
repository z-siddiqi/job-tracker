from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Job

# Create your views here.
def all_applications_view(request):
    all_applications = Job.objects.filter(user=request.user)
    context = {'applications_list': all_applications}
    return render(request, 'applications_list.html', context)

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'application_edit.html'
    fields = ('company',
        'title', 
        'url', 
        'deadline', 
        'progress', 
        'notes'
    )
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'application_delete.html'
    context_object_name = 'application'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'application_new.html'
    fields = ('company',
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