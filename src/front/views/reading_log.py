import logging

from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from core.models import ReadingLog
from core.filters import ReadingLogFilter
from front.forms.reading_log import ReadingLogForm
from .mixins import PaginationPageSizeMixin

logger = logging.getLogger(__name__)


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


class ReadingLogDetailView(DetailView):
    """Детальная страница ReadingLog (read-only)."""

    model = ReadingLog
    template_name = 'reading_log/readinglog_detail.html'
    context_object_name = 'readinglog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug(f'Viewing ReadingLog detail: pk={self.object.pk}')
        return context


class ReadingLogUpdateView(UpdateView):
    """Страница редактирования ReadingLog."""

    model = ReadingLog
    form_class = ReadingLogForm
    template_name = 'reading_log/readinglog_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readinglog'] = self.object
        return context

    def get_success_url(self):
        """Возврат на детальную страницу после успешного сохранения."""
        logger.info(f'Updated ReadingLog: pk={self.object.pk}')
        return reverse('readinglog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        logger.debug(f'Valid form submitted for ReadingLog: pk={self.object.pk}')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f'Invalid form submitted for ReadingLog: pk={self.object.pk}')
        return super().form_invalid(form)
