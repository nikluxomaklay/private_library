"""
Views для работы с заметками (Note) и ключевыми словами (KeyWord).

Этот модуль содержит:
- NoteListView для отображения списка заметок с иерархией
- NoteDetailView для отображения детальной страницы заметки
- NoteNewView для создания новых заметок
- Autocomplete views для использования с django-autocomplete-light
"""

from dal import autocomplete
from django.db import transaction
from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django_filters.views import FilterView

from core.models import Note, KeyWord
from core.filters import NoteFilter
from front.forms.notes import NoteForm, NoteToBookEditionFormSet
from .mixins import PaginationPageSizeMixin


class NoteListView(PaginationPageSizeMixin, FilterView):
    """
    View для отображения списка заметок с иерархической структурой.
    
    Отображает только верхнеуровневые заметки (без parent),
    с возможностью просмотра дочерних заметок с отступами.
    """
    model = Note
    filterset_class = NoteFilter
    template_name = 'notes/note_list.html'
    ordering = ['created_at']
    queryset = Note.objects.filter(
        parent__isnull=True
    ).prefetch_related('children')
    
    def get_template_names(self):
        """
        Возвращает список имён шаблонов для поиска.
        
        Переопределяем метод, чтобы использовать только основной шаблон
        и не добавлять fallback шаблон от FilterView.
        """
        return [self.template_name]
    
    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.
        
        Передаёт:
        - filter: объект filterset для отображения формы фильтрации
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class NoteDetailView(DetailView):
    """
    View для отображения детальной страницы заметки.

    Отображает все поля заметки:
    - Индекс, тема, текст
    - Родительская заметка (ссылкой)
    - Связанные книжные издания с additional_info
    - Ключевые слова
    - Связанные заметки
    - Даты создания и обновления
    """
    model = Note
    template_name = 'notes/note_detail.html'

    def get_queryset(self):
        """
        Возвращает queryset с оптимизированной загрузкой связанных данных.

        Использует select_related для parent и prefetch_related для:
        - keywords (M2M ключевые слова)
        - related_notes (M2M связанные заметки)
        - book_editions__book_edition (связи с книжными изданиями)
        """
        return Note.objects.select_related('parent').prefetch_related(
            'keywords',
            'related_notes',
            'book_editions__book_edition'
        )


class NoteNewView(CreateView):
    """
    View для создания новой заметки.

    Обрабатывает:
    - Основную форму NoteForm
    - Inline formset NoteToBookEditionFormSet для связей с книжными изданиями
    
    Поддерживает pre-fill полей из query параметров:
    - book_edition: ID книжного издания для предзаполнения formset
    - parent: ID родительской заметки для предзаполнения parent, book_editions, keywords
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_new.html'

    def get_initial(self):
        """
        Возвращает начальные данные для формы из query параметров.
        
        Поддерживает:
        - book_edition: предзаполнение book_editions в formset
        - parent: предзаполнение parent, book_editions, keywords из родительской заметки
        """
        initial = super().get_initial()
        
        # Pre-fill из book_edition query param
        book_edition_id = self.request.GET.get('book_edition')
        if book_edition_id:
            initial['book_editions'] = [int(book_edition_id)]
        
        # Pre-fill из parent query param
        parent_id = self.request.GET.get('parent')
        if parent_id:
            parent_note = Note.objects.get(pk=parent_id)
            initial['parent'] = parent_id
            # Копирование book_editions и keywords из parent
            initial['book_editions_initial'] = list(
                parent_note.book_editions.values_list('book_edition_id', flat=True)
            )
            initial['keywords_initial'] = list(
                parent_note.keywords.values_list('id', flat=True)
            )
        
        return initial

    def get_context_data(self, **kwargs):
        """
        Добавляет formset в контекст шаблона.
        
        Если есть query params для pre-fill, инициализируем formset с данными.
        """
        context = super().get_context_data(**kwargs)
        
        # Получаем initial данные для formset
        book_edition_id = self.request.GET.get('book_edition')
        parent_id = self.request.GET.get('parent')
        
        if self.request.POST:
            context['formset'] = NoteToBookEditionFormSet(self.request.POST)
        else:
            # Инициализируем formset с pre-filled данными
            initial_data = []
            
            # Pre-fill из book_edition
            if book_edition_id:
                initial_data.append({
                    'book_edition': int(book_edition_id),
                    'additional_info': '',
                })
            
            # Pre-fill из parent note (book_editions)
            elif parent_id:
                parent_note = Note.objects.get(pk=parent_id)
                for ntb in parent_note.book_editions.all():
                    initial_data.append({
                        'book_edition': ntb.book_edition_id,
                        'additional_info': '',
                    })
            
            if initial_data:
                context['formset'] = NoteToBookEditionFormSet(initial=initial_data)
            else:
                context['formset'] = NoteToBookEditionFormSet()
        
        return context

    def form_valid(self, form):
        """
        Обрабатывает валидную форму.

        - Сохраняет основную форму (Note)
        - Сохраняет formset с привязкой к note
        - Добавляет success message
        - Redirect на страницу детальной заметки
        """
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # Сохраняем основную форму
            self.object = form.save()

            # Сохраняем formset с привязкой к note
            formset.instance = self.object
            formset.save()

            # Добавляем success message
            messages.success(self.request, 'Заметка успешно создана')

            # Redirect на страницу детальной заметки
            return redirect('note_detail', pk=self.object.pk)

        return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Обрабатывает невалидную форму.

        Переопределяем для корректного отображения ошибок formset.
        """
        context = self.get_context_data()
        context['formset'] = context.get('formset', NoteToBookEditionFormSet())
        return self.render_to_response(context)


class NoteUpdateView(UpdateView):
    """
    View для обновления существующей заметки.

    Обрабатывает:
    - Основную форму NoteForm
    - Inline formset NoteToBookEditionFormSet для связей с книжными изданиями
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_update.html'

    def get_queryset(self):
        """
        Возвращает queryset с оптимизированной загрузкой связанных данных.

        Использует prefetch_related для book_editions.
        """
        return Note.objects.prefetch_related('book_editions')

    def get_context_data(self, **kwargs):
        """
        Добавляет formset в контекст шаблона.

        Если запрос POST, инициализируем formset с данными.
        Иначе создаем formset с existing instance.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = NoteToBookEditionFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['formset'] = NoteToBookEditionFormSet(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        """
        Обрабатывает валидную форму.

        - Сохраняет основную форму (Note)
        - Сохраняет formset с привязкой к note
        - Добавляет success message
        - Redirect на страницу детальной заметки
        """
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.save()

            messages.success(self.request, 'Заметка успешно обновлена')
            return redirect('note_detail', pk=self.object.pk)

        return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Обрабатывает невалидную форму.

        Переопределяем для корректного отображения ошибок formset.
        """
        context = self.get_context_data()
        context['formset'] = context.get('formset', NoteToBookEditionFormSet())
        return self.render_to_response(context)


class NoteDeleteView(DeleteView):
    """
    View для удаления существующей заметки.

    Проверяет наличие дочерних заметок перед удалением:
    - Если есть дети - блокирует удаление с error message
    - Если детей нет - удаляет заметку и redirect на список
    """
    model = Note
    template_name = 'notes/note_delete.html'
    success_url = reverse_lazy('note')

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос на удаление заметки.

        - Проверяет наличие дочерних заметок
        - Если дети есть - блокирует удаление с error message
        - Если детей нет - удаляет заметку и redirect на список
        """
        self.object = self.get_object()

        # Проверка на наличие дочерних заметок
        if self.object.children.exists():
            messages.error(
                request,
                'Нельзя удалить заметку с дочерними заметками. Сначала удалите или переместите дочерние заметки.'
            )
            return redirect('note_detail', pk=self.object.pk)

        # Удаление заметки (используем super для обхода ProtectedError)
        success_url = self.get_success_url()
        with transaction.atomic():
            self.object.book_editions.all().delete()
            self.object.delete()
        messages.success(request, 'Заметка успешно удалена')
        return redirect(success_url)


class NoteAutocompleteView(autocomplete.Select2QuerySetView):
    """
    Autocomplete view для модели Note.

    Поиск осуществляется по полям:
    - topic (тема заметки)
    - index (индекс заметки)
    """

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset заметок.

        Если есть поисковый запрос (self.q), фильтрует по topic или index.
        """
        qs = Note.objects.order_by('-created_at').all()
        if self.q:
            qs = qs.filter(
                Q(topic__istartswith=self.q) |
                Q(index__istartswith=self.q)
            )
        return qs


class KeyWordAutocompleteView(autocomplete.Select2QuerySetView):
    """
    Autocomplete view для модели KeyWord.

    Поиск осуществляется по полю word (ключевое слово).
    """

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset ключевых слов.

        Если есть поисковый запрос (self.q), фильтрует по word.
        """
        qs = KeyWord.objects.order_by('word').all()
        if self.q:
            qs = qs.filter(
                Q(word__istartswith=self.q)
            )
        return qs
