from django.urls import path

from .views import (
    board_detail, 
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
    path('new/', BoardCreateView.as_view(), name='board_new'),
    path('<int:board_pk>/', board_detail, name='board_detail'),
    path('<int:board_pk>/edit/', BoardUpdateView.as_view(), name='board_update'),
    path('<int:board_pk>/delete/', BoardDeleteView.as_view(), name='board_delete'),
    path('<int:board_pk>/jobs/new/', JobCreateView.as_view(), name='job_create'),
    path('<int:board_pk>/jobs/new/scrape/', scrape_job, name='scrape_job'),
    path('<int:board_pk>/jobs/<int:app_pk>/', JobUpdateView.as_view(), name='job_update'),
    path('<int:board_pk>/jobs/<int:app_pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
]
