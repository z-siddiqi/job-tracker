import shortuuid

from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from django_quill.fields import QuillField

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        default='',
        max_length=8,
    )

    def save(self, *args, **kwargs):
        # only generate slug on first save
        if not self.pk:
            rand_slug = str(shortuuid.uuid())[:8]
            self.slug = rand_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'board_slug': self.slug})

class Job(models.Model):  
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    deadline = models.DateField(default=now, blank=True)
    PROGRESS_CHOICES = (
        ('Applied', 'Applied'),
        ('Phone', 'Phone'),
        ('Onsite', 'Onsite'),
        ('Offer', 'Offer'),
    )
    progress = models.CharField(max_length=8, choices=PROGRESS_CHOICES, default='Applied')
    description = QuillField(blank=True, null=True)
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        default='',
        max_length=8,
    )

    class Meta:
        ordering = ['deadline', ]

    def save(self, *args, **kwargs):
        if not self.pk:
            rand_slug = str(shortuuid.uuid())[:8]
            self.slug = rand_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} at {self.company}'

    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'board_slug': self.board.slug})
