from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from chartjs.views.lines import BaseLineChartView

from boards.models import Board, Job
from utils.mixins import ajax_required, CustomLoginRequiredMixin

class MetricsMixin():
    
    def get_users_jobs(self, *args, **kwargs):
        boards = Board.objects.filter(user=self.request.user)
        jobs = Job.objects.filter(board__in=boards)
        return jobs


class MetricsView(CustomLoginRequiredMixin, MetricsMixin, TemplateView):
    template_name = 'metrics/metrics.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MetricsView, self).get_context_data(*args, **kwargs)
        jobs = self.get_users_jobs()
        context['recent_jobs'] = jobs.order_by('-updated_at')[:10]
        context['applied_count'] = jobs.filter(progress='Applied').count()
        context['phone_count'] = jobs.filter(progress='Phone').count()
        context['onsite_count'] = jobs.filter(progress='Onsite').count()
        context['offer_count'] = jobs.filter(progress='Offer').count()
        return context


class MetricsChartView(CustomLoginRequiredMixin, MetricsMixin, BaseLineChartView):

    def get_labels(self, *args, **kwargs):
        return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def get_providers(self, *args, **kwargs):
        return ['Jobs Added']

    def get_data(self, *args, **kwargs):
        current_year = datetime.now().strftime('%Y')
        jobs = self.get_users_jobs()
        jobs_added_this_year = jobs.filter(created_at__year=current_year)
        jobs_by_month = [(jobs_added_this_year.filter(created_at__month=str(x)).count()) for x in range(1, 13)]
        return [jobs_by_month]
    
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        return super(BaseLineChartView, self).get(request, *args, **kwargs)
