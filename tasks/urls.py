from django.urls import path

from .views import TaskListView, TaskCompleteView, TaskDeleteView

urlpatterns = [
    path('<str:job_slug>/', TaskListView.as_view(), name='task_list'),
    path('<int:task_pk>/complete/', TaskCompleteView.as_view(), name='task_complete'),
    path('<int:task_pk>/delete/', TaskDeleteView.as_view(), name='task_delete')
]
