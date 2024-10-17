from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from dal import autocomplete

from core.models import BookSeries


class BookSeriesListView(ListView):
    template_name = 'book_series/book_series_list.html'
    model = BookSeries
    ordering = ('publisher__name', 'name')


class BookSeriesNewView(CreateView):
    template_name = 'book_series/book_series_new.html'
    model = BookSeries
    fields = (
        'name',
        'publisher',
    )


class BookSeriesDetailView(DetailView):
    template_name = 'book_series/book_series_detail.html'
    model = BookSeries
    fields = (
        'name',
        'publisher',
    )


class BookSeriesUpdateView(UpdateView):
    template_name = 'book_series/book_series_update.html'
    model = BookSeries
    fields = (
        'name',
        'publisher',
    )


class BookSeriesDeleteView(DeleteView):
    model = BookSeries
    template_name = 'book_series/book_series_delete.html'
    success_url = reverse_lazy('book_series')
    fields = ()


class BookSeriesAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = BookSeries.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name__istartswith=self.q) |
                Q(publisher__name__istartswith=self.q),
            )
        return qs
