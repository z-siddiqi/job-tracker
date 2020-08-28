from django.urls import path

from .views import all_applications_view, ApplicationCreateView, ApplicationDeleteView, ApplicationUpdateView

urlpatterns = [
    path('', all_applications_view, name='applications_list'),
    path('new/', ApplicationCreateView.as_view(), name='application_new'),
    path('<int:pk>/detail', ApplicationUpdateView.as_view(), name='application_detail'),
    path('<int:pk>/delete', ApplicationDeleteView.as_view(), name='application_delete'),
]