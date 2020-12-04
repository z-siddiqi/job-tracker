from django.urls import path

from .views import MetricsView, MetricsChartView

urlpatterns = [
  path('', MetricsView.as_view(), name='metrics'),
  path('chart/', MetricsChartView.as_view(), name='metrics_chart'),
]