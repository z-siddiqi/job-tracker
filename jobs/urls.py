from django.urls import path

from .views import all_applications_view, job_results_view, ApplicationCreateView, ApplicationDeleteView, ApplicationUpdateView

urlpatterns = [
    path('', all_applications_view, name='applications_list'),
    path('search-results/', job_results_view, name='job_results'),
    path('new/', ApplicationCreateView.as_view(), name='application_new'),
    path('<int:pk>/detail', ApplicationUpdateView.as_view(), name='application_detail'),
    path('<int:pk>/delete', ApplicationDeleteView.as_view(), name='application_delete'),
]