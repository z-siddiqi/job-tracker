from datetime import datetime

from django.contrib.admin.models import LogEntry
from django.views.generic import TemplateView

from chartjs.views.lines import BaseLineChartView

from boards.models import Board, Job

class MetricsView(TemplateView):
    template_name = 'app/metrics.html'

    def get_users_jobs(self, *args, **kwargs):
        boards = Board.objects.filter(user=self.request.user)
        jobs = Job.objects.filter(board__in=boards)
        return jobs

    def get_context_data(self, *args, **kwargs):
        context = super(MetricsView, self).get_context_data(*args, **kwargs)
        jobs = self.get_users_jobs()
        context['recent_jobs'] = jobs.order_by('-updated_at')[:10]
        context['applied_count'] = jobs.filter(progress='Applied').count()
        context['phone_count'] = jobs.filter(progress='Phone').count()
        context['onsite_count'] = jobs.filter(progress='Onsite').count()
        context['offer_count'] = jobs.filter(progress='Offer').count()
        return context


class LineChartView(MetricsView, BaseLineChartView):

    def get_labels(self, *args, **kwargs):
        return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def get_providers(self, *args, **kwargs):
        return ['Jobs Added']

    def get_data(self, *args, **kwargs):
        current_year = datetime.now().strftime('%Y')
        jobs_added_this_year = self.get_users_jobs().filter(created_at__year=current_year)
        jobs_by_month = [(jobs_added_this_year.filter(created_at__month=str(x)).count()) for x in range(1, 13)]
        return [jobs_by_month]
