from django.db import models
from django.urls import reverse

from boards.models import Job
from tinymce.models import HTMLField

# Create your models here.
class Note(models.Model):
    note = HTMLField(verbose_name="", blank=True, null=True)
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse('note_update', kwargs={'app_pk': self.job.pk})
