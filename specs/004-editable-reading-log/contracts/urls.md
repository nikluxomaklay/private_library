# URL Contracts: Reading Log

**Feature**: 004-editable-reading-log  
**Date**: 6 марта 2026 г.

## URL Patterns

### New Routes

| URL Pattern | View | Name | Method | Description |
|-------------|------|------|--------|-------------|
| `/reading-log/<int:pk>/` | ReadingLogDetailView | `readinglog_detail` | GET | Детальная страница ReadingLog |
| `/reading-log/<int:pk>/update/` | ReadingLogUpdateView | `readinglog_update` | GET/POST | Страница редактирования ReadingLog |

### URL Configuration

**Location**: `src/core/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... existing patterns ...
    
    # Reading Log routes (new)
    path(
        'reading-log/<int:pk>/',
        views.ReadingLogDetailView.as_view(),
        name='readinglog_detail',
    ),
    path(
        'reading-log/<int:pk>/update/',
        views.ReadingLogUpdateView.as_view(),
        name='readinglog_update',
    ),
]
```

## View Contracts

### ReadingLogDetailView

**Purpose**: Отображение детальной информации о ReadingLog в режиме read-only

**Type**: Django DetailView

**Configuration**:
```python
class ReadingLogDetailView(DetailView):
    model = ReadingLog
    template_name = 'core/readinglog_detail.html'
    context_object_name = 'readinglog'
```

**Context**:
| Variable | Type | Description |
|----------|------|-------------|
| `readinglog` | ReadingLog | Объект ReadingLog |
| `object` | ReadingLog | Алиас на readinglog |

**GET Response**:
- **Status**: 200 OK
- **Template**: `core/readinglog_detail.html`
- **Context**: readinglog, object

**Error Responses**:
- **Status**: 404 Not Found
- **Condition**: ReadingLog с указанным pk не существует

---

### ReadingLogUpdateView

**Purpose**: Редактирование полей ReadingLog

**Type**: Django UpdateView

**Configuration**:
```python
class ReadingLogUpdateView(UpdateView):
    model = ReadingLog
    form_class = ReadingLogForm
    template_name = 'core/readinglog_form.html'
    success_url = reverse_lazy('readinglog_detail')  # Redirect to detail after success
    
    def get_success_url(self):
        """Возврат на детальную страницу отредактированного объекта"""
        return reverse('readinglog_detail', kwargs={'pk': self.object.pk})
```

**Context**:
| Variable | Type | Description |
|----------|------|-------------|
| `form` | ReadingLogForm | Форма редактирования |
| `object` | ReadingLog | Редактируемый объект |
| `readinglog` | ReadingLog | Алиас на object |

**GET Response**:
- **Status**: 200 OK
- **Template**: `core/readinglog_form.html`
- **Context**: form, object

**POST Response (Valid Data)**:
- **Status**: 302 Found (Redirect)
- **Location**: `/reading-log/<pk>/`
- **Action**: Сохранение изменений

**POST Response (Invalid Data)**:
- **Status**: 200 OK
- **Template**: `core/readinglog_form.html`
- **Context**: form (с ошибками), object

**Error Responses**:
- **Status**: 404 Not Found
- **Condition**: ReadingLog с указанным pk не существует

---

## Template Contracts

### readinglog_detail.html

**Location**: `src/core/templates/core/readinglog_detail.html`

**Required Blocks**:
```django
{% extends 'base.html' %}

{% block content %}
    <!-- ReadingLog detail content -->
    <!-- Display fields: book_edition, year_start, month_start, year_finish, month_finish -->
    <!-- Action block: Update button, Cancel/Back button -->
{% endblock %}
```

**Context Variables**:
| Variable | Type | Description |
|----------|------|-------------|
| `readinglog` | ReadingLog | Объект ReadingLog |
| `object` | ReadingLog | Алиас на readinglog |

---

### readinglog_form.html

**Location**: `src/core/templates/core/readinglog_form.html`

**Required Blocks**:
```django
{% extends 'base.html' %}

{% block content %}
    <!-- Form for editing ReadingLog -->
    <!-- Fields: year_start, month_start, year_finish, month_finish -->
    <!-- Submit button, Cancel button -->
{% endblock %}
```

**Context Variables**:
| Variable | Type | Description |
|----------|------|-------------|
| `form` | ReadingLogForm | Форма с полями |
| `object` | ReadingLog | Редактируемый объект |

---

## Integration Points

### Links to ReadingLog Detail

Следующие страницы должны содержать ссылки на детальную страницу ReadingLog:

1. **Home Page** (`/`)
   - Период ReadingLog → ссылка на `/reading-log/<pk>/`

2. **ReadingLog List** (если существует)
   - Период ReadingLog → ссылка на `/reading-log/<pk>/`

3. **BookEdition Detail** (`/book-edition/<pk>/`)
   - Период ReadingLog → ссылка на `/reading-log/<pk>/`
   - **Note**: Удалить текущие ссылки на год чтения

---

## Navigation Flow

```
[Home/ReadingLog List/BookEdition]
         ↓ (click period)
[ReadingLogDetailView] ←──┐
         ↓ (click Update)  │
[ReadingLogUpdateView] ────┘ (after save/cancel)
```
