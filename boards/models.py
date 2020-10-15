from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('home')

class Job(models.Model):  
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True, max_length=200, help_text = 'Don\'t forget to put "http://" at the beginning.')
    deadline = models.DateField(default=now, blank=True)
    PROGRESS_CHOICES = (
        ('Applied', 'Applied'),
        ('Phone', 'Phone'),
        ('Onsite', 'Onsite'),
        ('Offer', 'Offer'),
    )
    progress = models.CharField(max_length=8, choices=PROGRESS_CHOICES, default='AP')
    notes = models.TextField(blank=True, null=True)
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} at {self.company}'

    def get_absolute_url(self):
        return reverse('home')
