from django.db import models

from boards.models import Job
from tinymce.models import HTMLField

# Create your models here.
class Note(models.Model):
    note = HTMLField(verbose_name="", blank=True, null=True)
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
    )
