from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['completed', 'date']
    
    def __str__(self):
        return self.title
