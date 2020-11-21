import uuid
import shortuuid

from django.views.generic import View, CreateView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login

from .forms import CustomUserCreationForm
from .models import CustomUser 

from boards.demo import create_demo_board

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class GuestSignUpView(View):
    
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        guest_id = str(shortuuid.uuid())[:5]
        username = f"guest-{guest_id}"
        password = str(uuid.uuid4())

        # create guest account
        guest_user = User.objects.create_user(
            username=username,
            password=password,
            is_guest=True
        )

        # create demo board
        create_demo_board(guest_user)

        # log guest_user in
        guest_user = authenticate(username=username, password=password)
        login(request, guest_user)
        return redirect('board_list')

    def post(self, request, *args, **kwargs):
        return redirect('home')


class AccountDetailView(TemplateView):
    template_name = 'registration/account_detail.html'
