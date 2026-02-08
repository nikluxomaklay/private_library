from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from core.models import Year
from .mixins import PaginationPageSizeMixin


class YearListView(PaginationPageSizeMixin, ListView):
    template_name = 'year/year_list.html'
    model = Year
    ordering = '-year'


class YearNewView(CreateView):
    template_name = 'year/year_new.html'
    model = Year
    fields = (
        'year',
    )


class YearDetailView(DetailView):
    template_name = 'year/year_detail.html'
    model = Year
    fields = (
        'year',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset().order_by('-year')
        return context


class YearUpdateView(UpdateView):
    template_name = 'year/year_update.html'
    model = Year
    fields = (
        'year',
    )


class YearDeleteView(DeleteView):
    model = Year
    template_name = 'year/year_delete.html'
    success_url = reverse_lazy('year')
    fields = ()
