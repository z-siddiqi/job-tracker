from django.urls import path

from .views import (
    board_detail, 
    ApplicationCreateView, 
    ApplicationUpdateView, 
    application_delete, 
    BoardCreateView, 
    board_delete, 
)

urlpatterns = [
    path('new/', BoardCreateView.as_view(), name='board_new'),
    path('<int:board_pk>/', board_detail, name='board_detail'),
    path('<int:board_pk>/delete', board_delete, name='board_delete'),
    path('<int:board_pk>/jobs/new/', ApplicationCreateView.as_view(), name='application_new'),
    path('<int:board_pk>/jobs/<int:app_pk>/detail', ApplicationUpdateView.as_view(), name='application_detail'),
    path('<int:board_pk>/jobs/<int:app_pk>/delete', application_delete, name='application_delete'),
]
