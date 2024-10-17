from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from core.forms.book import BookForm
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
        'publisher',
        'series',
        'publication_year',
        'isbn',
    )


class BookUpdateView(UpdateView):
    template_name = 'book/book_update.html'
    model = Book
    fields = (
        'title',
        'extended_title',
        'authors',
        'publisher',
        'series',
        'publication_year',
        'isbn',
    )


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('book')
    fields = ()
