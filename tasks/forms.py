from django.forms import ModelForm
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FieldWithButtons

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("task",)
        labels = {"task": ""}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FieldWithButtons("task", Submit("submit", "Add", css_class="btn-dark"))
        )
