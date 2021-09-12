import emoji

from django.forms import ModelForm, ValidationError
from django.forms.widgets import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column, Submit, HTML
from crispy_forms.bootstrap import AppendedText

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
        fields = ("company", "logo", "title", "deadline", "progress", "description")
        labels = {"company": ""}
        widgets = {"description": SummernoteInplaceWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field("logo", type="hidden"),
            HTML(
                "<div class='position-relative d-inline-block'><img src='{% if job %}{{ job.logo }}{% else %}https://via.placeholder.com/130?text=Company+Logo{% endif %}' id='logo' class='img-fluid border rounded-2 mb-3'><span id='clear_logo' class='position-absolute top-0 end-0 cursor-pointer'><i class='bi bi-x fs-4'></i></span></div>"
            ),
            AppendedText(
                "company",
                "<div class='dropdown'><button id='company_dropdown_button' class='btn' type='button' data-bs-toggle='dropdown'><i class='bi bi-search'></i></button><ul class='dropdown-menu dropdown-menu-end' id='company_dropdown_menu'></ul></div>",
                placeholder="Enter a company name",
                autocomplete="off",
            ),
            Row(
                Column("title"),
                Column("progress"),
            ),
            "deadline",
            "description",
            Submit("submit", "Save", css_class="btn-dark"),
        )
