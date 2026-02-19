# Quickstart Guide: Zettelkasten Notes System

**Date**: 18 февраля 2026 г.
**Feature**: Zettelkasten Notes System
**Status**: ✅ **IMPLEMENTED** - Все функции реализованы

---

## Overview

Система заметок Zettelkasten интегрирована в существующее Django-приложение частной библиотеки. Заметки позволяют вести иерархические записи с связями с книжными изданиями и ключевыми словами.

**Реализованные функции**:
- ✅ Просмотр списка заметок с иерархией и пагинацией
- ✅ Детальная страница заметки
- ✅ Создание заметок (из списка, из книжного издания, из другой заметки)
- ✅ Редактирование заметок
- ✅ Удаление заметок с защитой от удаления родительских
- ✅ Связи с книжными изданиями через inline-формы
- ✅ Ключевые слова с autocomplete
- ✅ Иерархическая структура с автоматической генерацией индекса

---

## Быстрый старт для разработчика

### 1. Структура проекта

```
src/
├── core/
│   ├── models.py          # Note, NoteToBookEdition, KeyWord (уже существуют)
│   └── admin.py           # Admin interface (требуется реализация)
├── front/
│   ├── views/notes.py     # Views для CRUD операций
│   ├── forms/notes.py     # Формы
│   ├── urls.py            # URL маршруты (требуется добавить)
│   └── templates/notes/   # Templates
└── tests/
    ├── unit/
    └── integration/
```

### 2. Основные команды

```bash
# Запуск разработки
python src/manage.py runserver

# Запуск тестов
python src/manage.py test core.tests.test_note
python src/manage.py test front.tests.test_notes

# Применение миграций (уже существуют)
python src/manage.py migrate

# Создание суперпользователя (для admin)
python src/manage.py createsuperuser
```

### 3. Реализация (порядок выполнения)

1. **Models** - уже реализованы в `core/models.py`
2. **Admin** - зарегистрировать модели в `core/admin.py`
3. **Filters** - создать `core/filters.py` NoteFilter
4. **Forms** - создать `front/forms/notes.py`
5. **Views** - создать `front/views/notes.py`
6. **URLs** - добавить маршруты в `front/urls.py`
7. **Templates** - создать шаблоны в `src/templates/notes/`
8. **Tests** - написать тесты (TDD)

### 4. Ключевые паттерны

#### Autocomplete (django-autocomplete-light)

```python
# View
class NoteAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Note.objects.all()
        if self.q:
            qs = qs.filter(topic__istartswith=self.q)
        return qs

# Form widget
widgets = {
    'parent': autocomplete.Select2(
        url='note_autocomplete',
        attrs={"data-theme": "bootstrap-5"}
    ),
}
```

#### Inline formset для NoteToBookEdition

```python
from django.forms.models import inlineformset_factory

NoteToBookEditionFormSet = inlineformset_factory(
    Note,
    NoteToBookEdition,
    fields=('book_edition', 'additional_info'),
    extra=1,
    can_delete=True,
)
```

#### Пагинация

```python
class NoteListView(PaginationPageSizeMixin, FilterView):
    model = Note
    template_name = 'notes/note_list.html'
    ordering = 'index'
    # DEFAULT_PAGE_SIZE = 25
```

### 5. URL маршруты

Добавить в `front/urls.py`:

```python
from front.views import notes

urlpatterns = [
    # ... existing patterns ...
    
    path('note/', notes.NoteListView.as_view(), name='note'),
    path('note/new/', notes.NoteNewView.as_view(), name='note_new'),
    path('note/<int:pk>/', notes.NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/update/', notes.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', notes.NoteDeleteView.as_view(), name='note_delete'),
    path('note/autocomplete/', notes.NoteAutocompleteView.as_view(), name='note_autocomplete'),
    path('keyword/autocomplete/', notes.KeyWordAutocompleteView.as_view(), name='keyword_autocomplete'),
]
```

### 6. Templates

Базовая структура:

```html
{% extends 'base_layout.html' %}

{% block content %}
<div class="container">
    <h1>{% block title %}{% endblock %}</h1>
    
    <!-- Actions -->
    <div class="mb-3">
        <a href="{% url 'note_new' %}" class="btn btn-primary">New note</a>
    </div>
    
    <!-- Content -->
    {% block detail %}{% endblock %}
</div>
{% endblock %}
```

### 7. Проверка циклических зависимостей

```python
def check_circular_dependency(note, parent):
    """Проверка на циклическую зависимость."""
    if not parent:
        return True
    
    current = parent
    while current:
        if current == note:
            return False  # Цикл обнаружен
        current = current.parent
    return True
```

---

## User Scenarios

### Сценарий 1: Создание заметки из списка

1. Перейти в раздел "Notes" бокового меню
2. Нажать кнопку "New note"
3. Заполнить:
   - Тема (обязательно)
   - Текст (опционально)
   - Родительская заметка (опционально, autocomplete)
   - Книжные издания (опционально, inline-список)
   - Ключевые слова (опционально, autocomplete)
4. Нажать "Save"

### Сценарий 2: Создание заметки из книжного издания

1. Открыть детальную страницу книжного издания
2. Нажать кнопку "New note"
3. Поле "Книжное издание" предзаполнено текущим изданием
4. Заполнить остальные поля
5. Нажать "Save"

### Сценарий 3: Создание дочерней заметки

1. Открыть детальную страницу родительской заметки
2. Нажать кнопку "New note"
3. Поля "Родительская заметка", "Книжное издание", "Ключевые слова" предзаполнены
4. Поля "Тема" и "Текст" пустые
5. Заполнить тему и текст
6. Нажать "Save"

---

## Testing Checklist

- [ ] Создание заметки с темой
- [ ] Создание заметки без темы (ошибка валидации)
- [ ] Создание дочерней заметки
- [ ] Попытка создания циклической зависимости (ошибка)
- [ ] Добавление книжного издания с additional_info
- [ ] Удаление элемента из inline-списка
- [ ] Игнорирование пустых элементов inline-списка
- [ ] Предзаполнение полей при создании из book edition
- [ ] Предзаполнение полей при создании из заметки
- [ ] Удаление заметки без дочерних
- [ ] Попытка удаления заметки с дочерними (ошибка)
- [ ] Autocomplete для parent note
- [ ] Autocomplete для keywords
- [ ] Пагинация списка (25 на страницу)
- [ ] Отображение иерархии с отступами

---

## Ссылки

- [Spec](spec.md) - Feature specification ✅
- [Research](research.md) - Research & discovery ✅
- [Data Model](data-model.md) - Data model documentation ✅
- [API Contracts](contracts/api-contracts.md) - API contracts ✅
- [Tasks](tasks.md) - Implementation tasks ✅ COMPLETED

---

## Implementation Status

**Все функции реализованы**: 18 февраля 2026 г.

- ✅ Phase 1: Setup (T001-T003)
- ✅ Phase 2: Foundational (T004-T008)
- ✅ Phase 3: US1 - Список заметок (T009-T018)
- ✅ Phase 4: US2 - Детальная страница (T019-T026)
- ✅ Phase 5: US3 - Заметки на странице издания (T027-T032)
- ✅ Phase 6: US4 - Создание из списка (T033-T047)
- ✅ Phase 7: US5 - Создание из издания (T048-T051)
- ✅ Phase 8: US6 - Создание из заметки (T052-T056)
- ✅ Phase 9: US7 - Редактирование (T057-T068)
- ✅ Phase 10: US8 - Удаление (T069-T077)
- ✅ Phase N: Polish (T078-T085)
