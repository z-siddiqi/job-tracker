from django.forms import ModelForm

from .models import Board, Job

class BoardForm(ModelForm):

	class Meta:
		model = Board
		fields = ('title', )


class JobForm(ModelForm):

	class Meta:
		model = Job
		fields = (
			'company', 
			'title', 
			'deadline', 
			'progress', 
			'description'
    	)
