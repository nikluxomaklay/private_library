# Data Model: Zettelkasten Notes System

**Date**: 17 февраля 2026 г.
**Feature**: Zettelkasten Notes System

---

## Existing Models

Модели уже реализованы в `src/core/models.py`. Миграция существует.

### Note

Основная модель заметок системы Zettelkasten.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| index | TextField | db_index=True, unique=True | Индекс заметки (генерируется автоматически) |
| parent | ForeignKey(self) | on_delete=PROTECT, null, blank | Родительская заметка |
| related_notes | M2M(self) | - | Связанные заметки |
| keywords | M2M(KeyWord) | related_name='notes' | Ключевые слова |
| topic | CharField | max_length=255, not null | Тема заметки |
| text | TextField | null, blank | Текст заметки |
| created_at | DateTimeField | auto_now-add=True | Дата создания |
| updated_at | DateTimeField | auto_now=True | Дата обновления |

**Методы**:
- `save_base()`: Генерирует индекс при создании
- `__str__()`: Возвращает "{index} {topic}"

**Ограничения**:
- `on_delete=PROTECT` для parent - блокирует удаление родительской заметки
- Циклические зависимости должны блокироваться при сохранении

### NoteToBookEdition

Промежуточная модель для связи заметок с книжными изданиями.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| note | ForeignKey(Note) | on_delete=PROTECT, related_name='book_editions' | Заметка |
| book_edition | ForeignKey(BookEdition) | on_delete=PROTECT, related_name='notes' | Книжное издание |
| additional_info | TextField | null, blank | Дополнительная информация |

### KeyWord

Модель ключевых слов.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| word | CharField | max_length=255, not null | Ключевое слово |

---

## Entity Relationships

```
┌─────────────┐
│    Note     │
│             │
│ - index     │
│ - parent    │──┐ (self-referential, hierarchy)
│ - topic     │  │
│ - text      │  │
│ - keywords  │──┼── M2M ──┐
│             │  │         │
└─────────────┘  │         ▼
        │        │    ┌───────────┐
        │        └───▶│  KeyWord  │
        │             │           │
        │             │ - word    │
        ▼             └───────────┘
┌─────────────────┐
│NoteToBookEdition│
│                 │
│ - additional_info
│                 │
└────────┬────────┘
         │
         │ FK
         ▼
  ┌──────────────┐
  │ BookEdition  │
  │ (existing)   │
  └──────────────┘
```

---

## Validation Rules

### Note

| Field | Rule | Error Message |
|-------|------|---------------|
| topic | Required, max 255 chars | "Тема обязательна и не должна превышать 255 символов" |
| parent | No circular dependencies | "Нельзя создать циклическую зависимость в иерархии заметок" |
| index | Auto-generated, unique | Генерируется автоматически |

### NoteToBookEdition

| Field | Rule | Error Message |
|-------|------|---------------|
| book_edition | Required if additional_info provided | "Книжное издание обязательно для заполнения" |
| additional_info | Optional | - |

### KeyWord

| Field | Rule | Error Message |
|-------|------|---------------|
| word | Required, max 255 chars | "Ключевое слово обязательно и не должно превышать 255 символов" |

---

## State Transitions

### Note Lifecycle

```
[Create] ──▶ index generated ──▶ [Active] ──▶ [Update] ──▶ updated_at refreshed
                                     │
                                     ▼
                              [Delete] (blocked if has children)
```

**Циклическая зависимость**:
- Проверка при создании/обновлении
- Алгоритм: обход графа от parent вверх, проверка на возврат к текущей заметке

---

## Index Generation

Алгоритм генерации индекса реализован в `core.helpers.generate_note_number`.

**Принцип работы**:
- Для верхнеуровневых заметок: последовательная нумерация (1, 2, 3...)
- Для дочерних: иерархическая нумерация (1.1, 1.2, 2.1...)

---

## Query Patterns

### Основные запросы

1. **Получить верхнеуровневые заметки** (для пагинации):
```python
Note.objects.filter(parent__isnull=True).order_by('index')
```

2. **Получить дочерние заметки**:
```python
Note.objects.filter(parent=parent_note).order_by('index')
```

3. **Получить заметку со всеми связями**:
```python
Note.objects.select_related(
    'parent'
).prefetch_related(
    'keywords',
    'related_notes',
    'book_editions__book_edition'
).get(pk=pk)
```

4. **Получить заметки для книжного издания**:
```python
Note.objects.filter(
    book_editions__book_edition=book_edition
).select_related('parent').order_by('index')
```

---

## Database Constraints

- **Unique constraint** на `index` поле
- **Index** на `index` поле для ускорения сортировки
- **PROTECT** на всех FK для предотвращения случайного удаления связанных записей
