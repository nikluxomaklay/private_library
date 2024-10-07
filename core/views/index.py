from django.views.generic import TemplateView

from core.models import ReadingLog


class IndexPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['last_reading_logs'] = ReadingLog.objects.order_by(
            '-year_finish', '-month_finish', '-year_start', '-month_start',
        )[:10]

        return context
