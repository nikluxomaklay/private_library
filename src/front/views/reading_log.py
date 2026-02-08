from django.views.generic import CreateView, ListView

from core.models import ReadingLog
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


class ReadingLogListView(PaginationPageSizeMixin, ListView):
    template_name = 'reading_log/reading_log_list.html'
    model = ReadingLog
    ordering = ['-year_finish', '-month_finish', '-year_start', '-month_start']
