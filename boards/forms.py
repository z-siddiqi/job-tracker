import emoji

from django.forms import ModelForm, ValidationError

from .models import Board, Job
from .widgets import EmojiButton

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
        labels = {"icon" : ""}
        widgets = {"icon": EmojiButton(attrs={"class": "bg-transparent fs-3 grey-hover"})}


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ("company", "title", "deadline", "progress", "description")
        widgets = {"description": SummernoteInplaceWidget()}
