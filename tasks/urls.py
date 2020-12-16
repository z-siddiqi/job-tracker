from django.urls import path

from .views import TaskCreateView, TaskCompleteView, TaskDeleteView

urlpatterns = [
    path('<str:job_slug>/', TaskCreateView.as_view(), name='task_create'),
    path('<int:task_pk>/complete/', TaskCompleteView.as_view(), name='task_complete'),
    path('<int:task_pk>/delete/', TaskDeleteView.as_view(), name='task_delete')
]
