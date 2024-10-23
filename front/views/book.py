from dal import autocomplete
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from front.forms.book import BookForm
from core.models import Book


class BookListView(ListView):
    template_name = 'book/book_list.html'
    model = Book
    ordering = 'title'


class BookNewView(CreateView):
    template_name = 'book/book_new.html'
    model = Book
    form_class = BookForm


class BookDetailView(DetailView):
    template_name = 'book/book_detail.html'
    model = Book
    fields = (
        'title',
        'extended_title',
        'authors',
    )


class BookUpdateView(UpdateView):
    template_name = 'book/book_update.html'
    model = Book
    fields = (
        'title',
        'extended_title',
        'authors',
    )


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('book')
    fields = ()


class BookAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Book.objects.all()
        if self.q:
            qs = qs.filter(
                Q(title__istartswith=self.q) |
                Q(extended_title__istartswith=self.q) |
                Q(title_original__istartswith=self.q) |
                Q(extended_title_original__istartswith=self.q)
            )
        return qs
