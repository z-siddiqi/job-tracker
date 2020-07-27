from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .models import CustomUser 

# Create your views here.
class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')