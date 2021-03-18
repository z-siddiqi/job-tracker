from django.db import models

from boards.models import Job


class Task(models.Model):
    task = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    job = models.ForeignKey(
        Job,
        related_name="tasks",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = [
            "date",
        ]

    def __str__(self):
        return self.task
