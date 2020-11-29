from django.db import models
from django.urls import reverse

from boards.models import Job
from django_quill.fields import QuillField

# Create your models here.
class Note(models.Model):
    note = QuillField(verbose_name="", blank=True, null=True)
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
    )
