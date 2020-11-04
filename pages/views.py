from django.views.generic import TemplateView
from django.shortcuts import render


def custom_handler404(request, exception):
    return render(request, '404.html', status=404)


def custom_handler500(request):
    return render(request, '500.html', status=500)


class HomePageView(TemplateView):
    template_name = 'home.html'
