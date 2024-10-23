from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from core.models import BookEdition
from front.forms.book_edition import BookEditionNewForm
from front.forms.book_edition import BookEditionUpdateForm


class BookEditionListView(ListView):
    template_name = 'book_edition/book_edition_list.html'
    model = BookEdition
    ordering = 'book__title'


class BookEditionNewView(CreateView):
    template_name = 'book_edition/book_edition_new.html'
    model = BookEdition
    form_class = BookEditionNewForm


class BookEditionDetailView(DetailView):
    template_name = 'book_edition/book_edition_detail.html'
    model = BookEdition


class BookEditionUpdateView(UpdateView):
    template_name = 'book_edition/book_edition_update.html'
    model = BookEdition
    form_class = BookEditionUpdateForm


class BookEditionDeleteView(DeleteView):
    model = BookEdition
    template_name = 'book_edition/book_edition_delete.html'
    success_url = reverse_lazy('book_edition')
    fields = ()
