from django.urls import path

from .views import (
    board_detail, 
    ApplicationCreateView, 
    ApplicationUpdateView, 
    ApplicationDeleteView, 
    BoardCreateView, 
    BoardUpdateView, 
    BoardDeleteView, 
    scrape_job, 
)

urlpatterns = [
    path('new/', BoardCreateView.as_view(), name='board_new'),
    path('<int:board_pk>/', board_detail, name='board_detail'),
    path('<int:board_pk>/edit/', BoardUpdateView.as_view(), name='board_update'),
    path('<int:board_pk>/delete/', BoardDeleteView.as_view(), name='board_delete'),
    path('<int:board_pk>/jobs/new/', ApplicationCreateView.as_view(), name='application_new'),
    path('<int:board_pk>/jobs/new/scrape/', scrape_job, name='scrape_job'),
    path('<int:board_pk>/jobs/<int:app_pk>/', ApplicationUpdateView.as_view(), name='application_detail'),
    path('<int:board_pk>/jobs/<int:app_pk>/delete/', ApplicationDeleteView.as_view(), name='application_delete'),
]
