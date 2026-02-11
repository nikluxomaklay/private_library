from django.views.generic import CreateView
from django_filters.views import FilterView

from core.models import ReadingLog
from core.filters import ReadingLogFilter
from .mixins import PaginationPageSizeMixin


class ReadingLogNewView(CreateView):
    template_name = 'reading_log/reading_log_new.html'
    model = ReadingLog
    fields = (
        'book_edition',
        'year_start',
        'month_start',
        'year_finish',
        'month_finish',
    )

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.request.GET)
        return initial


class ReadingLogListView(PaginationPageSizeMixin, FilterView):
    template_name = 'reading_log/reading_log_list.html'
    model = ReadingLog
    filterset_class = ReadingLogFilter
    ordering = ['-year_finish', '-month_finish', '-year_start', '-month_start']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context
