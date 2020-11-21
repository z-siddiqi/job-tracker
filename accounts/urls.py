from django.urls import path

from .views import SignUpView, GuestSignUpView, AccountDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/guest', GuestSignUpView.as_view(), name='guest_signup'),
    path('user/', AccountDetailView.as_view(), name='account_detail'),
]