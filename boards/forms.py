import emoji

from django.forms import ModelForm, ValidationError
from django.forms.widgets import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from .models import Board, Job

from summernote.widgets import SummernoteInplaceWidget


class BoardForm(ModelForm):
    def clean_icon(self):
        icon = self.cleaned_data["icon"]
        if icon not in emoji.UNICODE_EMOJI["en"]:
            raise ValidationError("Icon needs to be an emoji.")
        return icon

    class Meta:
        model = Board
        fields = ("icon", "title")
        labels = {"icon": ""}
        widgets = {"icon": TextInput(attrs={"type": "button", "class": "bg-transparent fs-3 grey-hover"})}


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ("company", "title", "deadline", "progress", "description")
        widgets = {"description": SummernoteInplaceWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column("company"),
                Column("title"),
            ),
            Row(
                Column("deadline"),
                Column("progress"),
            ),
            "description",
            Submit("submit", "Save", css_class="btn-dark"),
        )
