# API Contracts: Zettelkasten Notes System

**Date**: 18 февраля 2026 г.
**Feature**: Zettelkasten Notes System
**Status**: ✅ **IMPLEMENTED** - Все view реализованы

---

## URL Patterns

### Primary Routes

| Method | URL | View | Description |
|--------|-----|------|-------------|
| GET | `/note/` | NoteListView | Список заметок (иерархический) |
| GET | `/note/new/` | NoteNewView | Форма создания заметки |
| POST | `/note/new/` | NoteNewView | Создание заметки |
| GET | `/note/<int:pk>/` | NoteDetailView | Детальная страница заметки |
| GET | `/note/<int:pk>/update/` | NoteUpdateView | Форма редактирования заметки |
| POST | `/note/<int:pk>/update/` | NoteUpdateView | Сохранение изменений |
| GET | `/note/<int:pk>/delete/` | NoteDeleteView | Форма удаления заметки |
| POST | `/note/<int:pk>/delete/` | NoteDeleteView | Удаление заметки |

### Autocomplete Routes

| Method | URL | View | Description |
|--------|-----|------|-------------|
| GET | `/note/autocomplete/` | NoteAutocompleteView | Autocomplete для заметок (parent) |
| GET | `/book/autocomplete/` | BookAutocompleteView | Autocomplete для книг (существующий) |
| GET | `/keyword/autocomplete/` | KeyWordAutocompleteView | Autocomplete для ключевых слов |

---

## View Contracts

### NoteListView

**Template**: `notes/note_list.html`

**Query Parameters**:
- `page` (int): Номер страницы
- `page_size` (int): Размер страницы (10, 25, 50, 100; default: 25)

**Context**:
- `object_list`: QuerySet верхнеуровневых заметок с дочерними
- `filter`: FilterSet для фильтрации (если есть)
- `page_size_choices`: [10, 25, 50, 100]
- `page_size_selected`: Выбранный размер страницы

**Behavior**:
- Пагинация применяется только к верхнеуровневым заметкам
- Дочерние заметки отображаются все на той же странице
- Иерархия через отступы в template

---

### NoteDetailView

**Template**: `notes/note_detail.html`

**URL**: `/note/<int:pk>/`

**Context**:
- `object`: Note instance
- `note.index`: Индекс заметки
- `note.topic`: Тема
- `note.text`: Текст
- `note.parent`: Родительская заметка (если есть)
- `note.book_editions.all`: Связанные книжные издания с additional_info
- `note.keywords.all`: Ключевые слова
- `note.related_notes.all`: Связанные заметки
- `note.created_at`, `note.updated_at`: Даты

---

### NoteNewView / NoteUpdateView

**Templates**: `notes/note_new.html`, `notes/note_update.html`

**Form**: NoteForm с inline formset для NoteToBookEdition

**Fields**:
- `topic` (CharField, required, max_length=255)
- `text` (TextField, optional)
- `parent` (autocomplete.Select2, optional)
- `keywords` (autocomplete.Select2Multiple, optional)
- `book_editions` (inline formset):
  - `book_edition` (autocomplete.Select2, optional)
  - `additional_info` (TextField, optional, disabled if no book_edition)

**Validation**:
- Topic required, max 255 chars
- Circular dependency check на parent
- Empty book_edition elements игнорируются

**Pre-fill Logic**:

| Source | Pre-filled Fields |
|--------|-------------------|
| Note list | None |
| Book edition detail | `book_editions` с текущим изданием |
| Note detail | `parent`, `book_editions`, `keywords` из исходной заметки |

**Success URL**: `note_detail` (pk=new_note.pk)

---

### NoteDeleteView

**Template**: `notes/note_delete.html`

**URL**: `/note/<int:pk>/delete/`

**Context**:
- `object`: Note instance для удаления

**Protection**:
- Если у заметки есть дочерние (children.exists()), удаление блокируется
- HTTP 400 с сообщением: "Невозможно удалить: есть дочерние заметки"
- on_delete=PROTECT на уровне модели также блокирует удаление

**Behavior**:
- GET: Отображает страницу подтверждения с информацией о заметке
- POST: Выполняет удаление или возвращает ошибку
- После успешного удаления перенаправляет на список заметок

**Success URL**: `note` (список заметок)

---

### Autocomplete Views

**NoteAutocompleteView**:
- QuerySet: Note.objects.all()
- Filter: topic__istartswith=self.q
- Display: f"{obj.index} {obj.topic}"

**KeyWordAutocompleteView**:
- QuerySet: KeyWord.objects.all()
- Filter: word__istartswith=self.q
- Display: obj.word

---

## Form Contracts

### NoteForm

```python
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('topic', 'text', 'parent', 'keywords')
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'parent': autocomplete.Select2(url='note_autocomplete', attrs={'data-theme': 'bootstrap-5'}),
            'keywords': autocomplete.Select2Multiple(url='keyword_autocomplete', attrs{'data-theme': 'bootstrap-5'}),
        }
```

### NoteToBookEditionFormSet

```python
NoteToBookEditionFormSet = inlineformset_factory(
    Note,
    NoteToBookEdition,
    fields=('book_edition', 'additional_info'),
    extra=1,
    can_delete=True,
    widgets={
        'book_edition': autocomplete.Select2(url='book_autocomplete', attrs={'data-theme': 'bootstrap-5'}),
        'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
    }
)
```

**Behavior**:
- `additional_info` disabled, если `book_edition` не выбран
- Пустые элементы (без book_edition) игнорируются при сохранении

---

## Error Responses

| Scenario | HTTP Status | Message |
|----------|-------------|---------|
| Circular dependency | 400 | "Нельзя создать циклическую зависимость в иерархии заметок" |
| Delete with children | 400 | "Невозможно удалить: есть дочерние заметки" |
| Topic required | 400 (form validation) | "Тема обязательна" |
| Topic too long | 400 (form validation) | "Тема не должна превышать 255 символов" |

---

## Context Data for Templates

### note_list.html

```python
{
    'object_list': List[Note],  # Верхнеуровневые с дочерними
    'filter': NoteFilter,  # Если есть фильтрация
    'page_size_choices': [10, 25, 50, 100],
    'page_size_selected': 25,
    'is_paginated': True,
}
```

### note_detail.html

```python
{
    'object': Note,
    'index': str,
    'topic': str,
    'text': str,
    'parent': Note or None,
    'book_editions': List[NoteToBookEdition],
    'keywords': List[KeyWord],
    'related_notes': List[Note],
    'created_at': datetime,
    'updated_at': datetime,
}
```

### note_new.html / note_update.html

```python
{
    'form': NoteForm,
    'formset': NoteToBookEditionFormSet,
    'title': "Создание заметки" / "Редактирование заметки",
}
```
