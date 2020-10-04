from django.urls import path

from .views import (
    board_detail, 
    ApplicationCreateView, 
    ApplicationDeleteView, 
    ApplicationUpdateView,
    BoardCreateView, 
    BoardDeleteView, 
)

urlpatterns = [
    path('new/', BoardCreateView.as_view(), name='board_new'),
    path('<int:pk>/detail', board_detail, name='board_detail'),
    path('<int:pk>/delete', BoardDeleteView.as_view(), name='board_delete'),
    path('jobs/new/', ApplicationCreateView.as_view(), name='application_new'),
    path('jobs/<int:pk>/detail', ApplicationUpdateView.as_view(), name='application_detail'),
    path('jobs/<int:pk>/delete', ApplicationDeleteView.as_view(), name='application_delete'),
]
