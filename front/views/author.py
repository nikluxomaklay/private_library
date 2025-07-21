from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from dal import autocomplete

from core.models import Author
from .mixins import PaginationPageSizeMixin


class AuthorListView(PaginationPageSizeMixin, ListView):
    template_name = 'author/author_list.html'
    model = Author
    ordering = 'last_name'


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
