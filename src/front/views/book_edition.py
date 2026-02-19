from dal import autocomplete
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView

from core.models import BookEdition, Note
from core.filters import BookEditionFilter
from front.forms.book_edition import BookEditionNewForm
from front.forms.book_edition import BookEditionUpdateForm
from .mixins import PaginationPageSizeMixin


class BookEditionListView(PaginationPageSizeMixin, FilterView):
    template_name = 'book_edition/book_edition_list.html'
    model = BookEdition
    filterset_class = BookEditionFilter
    ordering = 'book__title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class BookEditionNewView(CreateView):
    template_name = 'book_edition/book_edition_new.html'
    model = BookEdition
    form_class = BookEditionNewForm


class BookEditionDetailView(DetailView):
    template_name = 'book_edition/book_edition_detail.html'
    model = BookEdition

    def get_context_data(self, **kwargs):
        """
        Добавляет связанные заметки в контекст шаблона.

        Возвращает queryset заметок, связанных с данным book_edition,
        с оптимизированной загрузкой parent и children для иерархического отображения.
        """
        context = super().get_context_data(**kwargs)
        root_ids = Note.objects.filter(
            book_editions__book_edition=self.object
        ).values_list('id', 'root')
        root_ids = [item[0] if item[1] is None else item[1] for item in root_ids]
        context['notes'] = Note.objects.filter(
            id__in=root_ids,
        ).select_related(
            'parent', 'root',
        ).prefetch_related(
            'children',
        ).order_by('index', 'id')
        return context


class BookEditionUpdateView(UpdateView):
    template_name = 'book_edition/book_edition_update.html'
    model = BookEdition
    form_class = BookEditionUpdateForm


class BookEditionDeleteView(DeleteView):
    model = BookEdition
    template_name = 'book_edition/book_edition_delete.html'
    success_url = reverse_lazy('book_edition')
    fields = ()


class BookEditionAutocompleteView(autocomplete.Select2QuerySetView):
    """
    Autocomplete view для модели BookEdition.

    Поиск осуществляется по полям:
    - book__title (название книги)
    - publisher__name (название издательства)
    """

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset book_editions.

        Если есть поисковый запрос (self.q), фильтрует по title книги или publisher.
        """
        qs = BookEdition.objects.select_related('book', 'publisher').all()
        if self.q:
            qs = qs.filter(
                Q(book__title__istartswith=self.q) |
                Q(publisher__name__istartswith=self.q)
            )
        return qs
