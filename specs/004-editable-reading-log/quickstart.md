# Quickstart: Редактирование Reading Log

**Feature**: 004-editable-reading-log  
**Date**: 6 марта 2026 г.

## Быстрый старт для разработчика

Этот документ описывает минимальный набор изменений для реализации функциональности.

## Предварительные требования

- ✅ Ветка `004-editable-reading-log` активна
- ✅ Spec.md прочитан и понят
- ✅ Research.md изучен
- ✅ Data-model.md изучен

## Шаги реализации

### Шаг 1: Форма (src/core/forms.py)

```python
from django import forms
from core.models import ReadingLog


class ReadingLogForm(forms.ModelForm):
    """Форма для редактирования ReadingLog."""
    
    class Meta:
        model = ReadingLog
        fields = ['year_start', 'month_start', 'year_finish', 'month_finish']
    
    def clean(self):
        """
        Валидация: дата окончания не может быть раньше даты начала.
        """
        cleaned_data = super().clean()
        year_start = cleaned_data.get('year_start')
        year_finish = cleaned_data.get('year_finish')
        month_start = cleaned_data.get('month_start')
        month_finish = cleaned_data.get('month_finish')
        
        if year_start and year_finish:
            if year_finish < year_start:
                raise forms.ValidationError(
                    "Год окончания не может быть раньше года начала"
                )
            elif year_finish == year_start and month_finish and month_start:
                if month_finish < month_start:
                    raise forms.ValidationError(
                        "Месяц окончания не может быть раньше месяца начала "
                        "в пределах одного года"
                    )
        
        return cleaned_data
```

---

### Шаг 2: Views (src/core/views.py)

```python
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from core.models import ReadingLog


class ReadingLogDetailView(DetailView):
    """Детальная страница ReadingLog (read-only)."""
    
    model = ReadingLog
    template_name = 'core/readinglog_detail.html'
    context_object_name = 'readinglog'


class ReadingLogUpdateView(UpdateView):
    """Страница редактирования ReadingLog."""
    
    model = ReadingLog
    form_class = ReadingLogForm
    template_name = 'core/readinglog_form.html'
    
    def get_success_url(self):
        """Возврат на детальную страницу после успешного сохранения."""
        return reverse('readinglog_detail', kwargs={'pk': self.object.pk})
```

---

### Шаг 3: URLs (src/core/urls.py)

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

---

### Шаг 4: Templates

#### src/core/templates/core/readinglog_detail.html

```django
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
<div class="container">
    <h1>Reading Log: {{ readinglog.period }}</h1>
    
    <div class="card">
        <div class="card-body">
            <dl class="row">
                <dt class="col-sm-3">Книга:</dt>
                <dd class="col-sm-9">{{ readinglog.book_edition }}</dd>
                
                <dt class="col-sm-3">Год начала:</dt>
                <dd class="col-sm-9">{{ readinglog.year_start|default:"—" }}</dd>
                
                <dt class="col-sm-3">Месяц начала:</dt>
                <dd class="col-sm-9">{{ readinglog.get_month_start_display|default:"—" }}</dd>
                
                <dt class="col-sm-3">Год окончания:</dt>
                <dd class="col-sm-9">{{ readinglog.year_finish|default:"—" }}</dd>
                
                <dt class="col-sm-3">Месяц окончания:</dt>
                <dd class="col-sm-9">{{ readinglog.get_month_finish_display|default:"—" }}</dd>
            </dl>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'readinglog_update' readinglog.pk %}" class="btn btn-primary">
            Update
        </a>
        <a href="javascript:history.back()" class="btn btn-secondary">
            Назад
        </a>
    </div>
</div>
{% endblock %}
```

#### src/core/templates/core/readinglog_form.html

```django
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block content %}
<div class="container">
    <h1>Редактировать Reading Log</h1>
    
    <form method="post">
        {% csrf_token %}
        {% bootstrap_form form %}
        
        <button type="submit" class="btn btn-success">Сохранить</button>
        <a href="{% url 'readinglog_detail' readinglog.pk %}" class="btn btn-secondary">
            Отмена
        </a>
    </form>
</div>
{% endblock %}
```

---

### Шаг 5: Обновление существующих templates

#### Home page (src/core/templates/core/home.html или аналог)

Найти отображение периода ReadingLog и заменить:

```django
<!-- Было -->
<span>{{ readinglog.period }}</span>

<!-- Стало -->
<a href="{% url 'readinglog_detail' readinglog.pk %}">
    {{ readinglog.period }}
</a>
```

#### BookEdition detail (src/core/templates/core/bookedition_detail.html)

Найти ссылки на год чтения и заменить на ссылку на ReadingLog:

```django
<!-- Было -->
<a href="{{ readinglog.year_start.get_absolute_url }}">{{ readinglog.year_start }}</a>

<!-- Стало -->
<a href="{% url 'readinglog_detail' readinglog.pk %}">
    {{ readinglog.period_for_template|safe }}
</a>
```

---

## Запуск и тестирование

### 1. Применить изменения

```bash
# Убедиться, что ветка активна
git branch

# Запустить сервер разработки
python src/manage.py runserver
```

### 2. Проверить маршруты

```bash
# Проверить, что URL разрешаются
python src/manage.py show_urls | grep readinglog
```

### 3. Ручное тестирование

1. Открыть `/` (Home)
2. Кликнуть на период ReadingLog → проверить переход на детальную страницу
3. Кликнуть "Update" → проверить открытие формы
4. Изменить поля → сохранить → проверить редирект и сохранение
5. Нажать "Отмена" → проверить редирект без сохранения
6. Ввести некорректные даты → проверить ошибку валидации

---

## Тесты (TDD)

**Следующий шаг**: После реализации создать тесты в `src/tests/integration/test_readinglog_views.py`

См. `/speckit.tasks` для создания задач по тестированию.
