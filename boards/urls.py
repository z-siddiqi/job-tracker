from django.urls import path

from .views import (
    BoardDetailView, 
    BoardListView, 
    JobCreateView, 
    JobUpdateView, 
    JobDeleteView, 
    BoardCreateView, 
    BoardUpdateView, 
    BoardDeleteView, 
    scrape_job, 
)

urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
    path('new/', BoardCreateView.as_view(), name='board_create'),
    path('<str:board_slug>/', BoardDetailView.as_view(), name='board_detail'),
    path('<str:board_slug>/edit/', BoardUpdateView.as_view(), name='board_update'),
    path('<str:board_slug>/delete/', BoardDeleteView.as_view(), name='board_delete'),
    path('<str:board_slug>/jobs/new/', JobCreateView.as_view(), name='job_create'),
    path('<str:board_slug>/jobs/new/scrape/', scrape_job, name='scrape_job'),
    path('<str:board_slug>/jobs/<str:job_slug>/edit', JobUpdateView.as_view(), name='job_update'),
    path('<str:board_slug>/jobs/<str:job_slug>/delete/', JobDeleteView.as_view(), name='job_delete'),
]
