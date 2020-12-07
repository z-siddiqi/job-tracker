from django.forms import ModelForm

from .models import Note

from summernote.widgets import SummernoteInplaceWidget

class NoteForm(ModelForm):

	class Meta:
		model = Note
		fields = ('note', )

		widgets = {
            'note': SummernoteInplaceWidget()
        }
