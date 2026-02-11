from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from dal import autocomplete
from django_filters.views import FilterView

from core.models import Author
from core.filters import AuthorFilter
from .mixins import PaginationPageSizeMixin


class AuthorListView(PaginationPageSizeMixin, FilterView):
    template_name = 'author/author_list.html'
    model = Author
    filterset_class = AuthorFilter
    ordering = 'last_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class AuthorNewView(CreateView):
    template_name = 'author/author_new.html'
    model = Author
    fields = (
        'first_name',
        'last_name',
        'middle_name',
    )


class AuthorDetailView(DetailView):
    template_name = 'author/author_detail.html'
    model = Author
    fields = (
        'first_name',
        'last_name',
        'middle_name',
    )


class AuthorUpdateView(UpdateView):
    template_name = 'author/author_update.html'
    model = Author
    fields = (
        'first_name',
        'last_name',
        'middle_name',
    )


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author/author_delete.html'
    success_url = reverse_lazy('author')
    fields = ()


class AuthorAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all()
        if self.q:
            qs = qs.filter(
                Q(first_name__istartswith=self.q) |
                Q(last_name__istartswith=self.q) |
                Q(middle_name__istartswith=self.q)
            )
        return qs
