# Research & Discovery: Zettelkasten Notes System

**Date**: 17 февраля 2026 г.
**Feature**: Zettelkasten Notes System

---

## Research Task 1: Селекторы с live-поиском (django-autocomplete-light)

### Findings

**Паттерн реализации autocomplete**:

1. **View** (на примере Publisher):
```python
class PublisherAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publisher.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
```

2. **Form Widget**:
```python
widgets = {
    'publisher': autocomplete.Select2(
        url='publisher_autocomplete',
        attrs={"data-theme": "bootstrap-5"}
    ),
}
```

3. **URL**:
```python
path('publisher/autocomplete/', publisher.PublisherAutocompleteView.as_view(), name='publisher_autocomplete'),
```

### Decision

Использовать тот же паттерн для Note, KeyWord, BookEdition:
- Создать autocomplete views в `front/views/notes.py`
- Добавить widgets в форму заметок
- Зарегистрировать URLs

### Alternatives Considered

- Использовать стандартный Select без autocomplete - отклонено, т.к. требует ручного ввода ID
- Использовать другие библиотеки autocomplete - отклонено, т.к. dal уже установлена и используется в проекте

---

## Research Task 2: CRUD views паттерны

### Findings

**Стандартная структура views**:

```python
class NoteListView(PaginationPageSizeMixin, FilterView):
    template_name = 'notes/note_list.html'
    model = Note
    filterset_class = NoteFilter
    ordering = 'index'

class NoteNewView(CreateView):
    template_name = 'notes/note_new.html'
    model = Note
    form_class = NoteForm

class NoteDetailView(DetailView):
    template_name = 'notes/note_detail.html'
    model = Note

class NoteUpdateView(UpdateView):
    template_name = 'notes/note_update.html'
    model = Note
    form_class = NoteUpdateForm

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'
    success_url = reverse_lazy('note')
```

### Decision

Следовать тому же паттерну для заметок.

### URL Patterns

Стандартный паттерн именования:
- `note/` → note_list
- `note/new/` → note_new
- `note/<int:pk>/` → note_detail
- `note/<int:pk>/delete/` → note_delete
- `note/<int:pk>/update/` → note_update
- `note/autocomplete/` → note_autocomplete

---

## Research Task 3: Пагинация

### Findings

**Миксин PaginationPageSizeMixin**:

```python
class PaginationPageSizeMixin:
    PAGE_SIZE_CHOICES = [10, 25, 50, 100]
    DEFAULT_PAGE_SIZE = 25

    def get_paginate_by(self, queryset):
        try:
            page_size = int(self.request.GET.get('page_size', self.DEFAULT_PAGE_SIZE))
            if page_size not in self.PAGE_SIZE_CHOICES:
                page_size = self.DEFAULT_PAGE_SIZE
        except (TypeError, ValueError):
            page_size = self.DEFAULT_PAGE_SIZE
        return page_size
```

### Decision

**Стандартный лимит пагинации: 25** (DEFAULT_PAGE_SIZE)

Использовать PaginationPageSizeMixin для всех list views заметок.

---

## Research Task 4: Структура templates

### Findings

**Структура директорий templates**:
```
src/templates/
├── base_layout.html      # Базовый шаблон
├── base_filter_form.html # Шаблон для форм фильтров
├── book/
│   ├── book_list.html
│   ├── book_detail.html
│   ├── book_new.html
│   ├── book_update.html
│   └── book_delete.html
└── ...
```

**Использование bootstrap5**:
- Формы используют `attrs={"class": "form-control"}` для полей
- Кнопки используют классы bootstrap
- Сетка через bootstrap grid system

### Decision

Создать структуру:
```
src/templates/notes/
├── note_list.html
├── note_detail.html
├── note_new.html
├── note_update.html
├── note_delete.html
└── _note_tree.html  # partial для иерархического отображения
```

---

## Research Task 5: M2M связи с additional info

### Findings

**Модель NoteToBookEdition**:
```python
class NoteToBookEdition(models.Model):
    note = models.ForeignKey('Note', on_delete=models.PROTECT, related_name='book_editions')
    book_edition = models.ForeignKey('BookEdition', on_delete=models.PROTECT, related_name='notes')
    additional_info = models.TextField(null=True, blank=True)
```

Это промежуточная модель для M2M связи с дополнительными данными.

### Паттерн для inline-форм

Требуется использовать Django formsets для обработки inline-связей:

```python
from django.forms.models import inlineformset_factory

NoteToBookEditionFormSet = inlineformset_factory(
    Note,
    NoteToBookEdition,
    fields=('book_edition', 'additional_info'),
    extra=1,
    can_delete=True
)
```

### Decision

Использовать formsets для обработки inline-списка книжных изданий в форме заметки.

---

## Summary: Technology Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Autocomplete | django-autocomplete-light (Select2) | Уже используется в проекте |
| Views | Class-based generic views | Стандарт проекта |
| Pagination | 25 items default | Стандарт проекта |
| Templates | Bootstrap 5 + django-bootstrap5 | Стандарт проекта |
| Inline forms | Django formsets | Стандартный подход для M2M с additional info |
| Filters | django-filter + BaseFilterSet | Уже используется в проекте |

---

## Next Steps

1. Создать модели (уже существуют)
2. Создать filters для Note
3. Создать forms для CRUD операций
4. Создать views для CRUD операций
5. Создать autocomplete views
6. Создать templates
7. Зарегистрировать URLs
8. Реализовать admin interface
9. Написать тесты (TDD)
