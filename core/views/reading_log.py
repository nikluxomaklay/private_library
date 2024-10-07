from django.views.generic import CreateView

from core.models import ReadingLog


class ReadingLogNewView(CreateView):
    template_name = 'reading_log/reading_log_new.html'
    model = ReadingLog
    fields = (
        'book',
        'year_start',
        'month_start',
        'year_finish',
        'month_finish',
    )

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.request.GET)
        return initial
