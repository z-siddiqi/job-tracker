from django.urls import path

from .views import TaskCreateView
from .api import TaskDetailView

urlpatterns = [
    path("", TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
]
