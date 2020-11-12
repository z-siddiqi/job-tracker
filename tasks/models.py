from django.db import models

from boards.models import Job

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['date', ]
    
    def __str__(self):
        return self.title
