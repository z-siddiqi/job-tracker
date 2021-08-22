from django.forms import ModelForm, TextInput

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("task",)
        widgets = {"task": TextInput(attrs={"class": "form-control", "id": "task"})}
