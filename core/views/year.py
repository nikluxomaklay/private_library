from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from core.models import Year


class YearListView(ListView):
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
