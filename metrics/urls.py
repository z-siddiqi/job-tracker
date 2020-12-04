from django.urls import path

from .views import MetricsView, LineChartView

urlpatterns = [
  path('', MetricsView.as_view(), name='metrics'),
  path('chart/', LineChartView.as_view(), name='metrics_chart'),
]