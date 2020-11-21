from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields
