# Research: Редактирование Reading Log

**Date**: 6 марта 2026 г.  
**Feature**: 004-editable-reading-log

## Phase 0: Outline & Research

### Extracted Unknowns from Technical Context

| Unknown | Context | Research Task |
|---------|---------|---------------|
| Существующие patterns для detail/update views | Django views для других моделей | Изучить существующие views в проекте |
| Формы с django-bootstrap5 | Формы редактирования | Изучить существующие формы |
| Валидация дат в Django forms | Валидация: дата окончания >= даты начала | Найти best practices |
| django-autocomplete-light для Year | Селекторы для Year field | Изучить интеграцию |

---

## Research Findings

### 1. Существующие patterns для views в проекте

**Decision**: Использовать классы Django CBV (Class-Based Views)

**Rationale**: 
- Проект уже использует CBV для существующих моделей
- DetailView и UpdateView предоставляют готовую функциональность
- Соответствует Django best practices

**Alternatives considered**:
- FBV (Function-Based Views) — отклонено: меньше переиспользования кода, сложнее поддержка

**Source**: Анализ существующего кода проекта

---

### 2. Формы с django-bootstrap5

**Decision**: Использовать django-bootstrap5 для рендеринга форм

**Rationale**:
- django-bootstrap5 уже подключен в проекте (requirements.txt)
- Единый стиль со всеми существующими формами
- Быстрая интеграция без дополнительного CSS

**Alternatives considered**:
- Кастомный рендеринг форм — отклонено: избыточная работа
- Другие CSS-фреймворки — отклонено: уже выбран bootstrap5

**Source**: requirements.txt, существующие templates проекта

---

### 3. Валидация дат в Django forms

**Decision**: Использовать clean() метод формы для кросс-полевой валидации

**Rationale**:
- Django предоставляет встроенный механизм валидации на уровне формы
- clean() позволяет сравнивать значения нескольких полей
- Ошибка отображается пользователю в понятном виде

**Implementation pattern**:
```python
def clean(self):
    cleaned_data = super().clean()
    year_start = cleaned_data.get('year_start')
    year_finish = cleaned_data.get('year_finish')
    month_start = cleaned_data.get('month_start')
    month_finish = cleaned_data.get('month_finish')
    
    # Валидация: если оба года указаны, finish >= start
    if year_start and year_finish:
        if year_finish < year_start:
            raise ValidationError("Дата окончания не может быть раньше даты начала")
        elif year_finish == year_start and month_finish and month_start:
            if month_finish < month_start:
                raise ValidationError("Месяц окончания не может быть раньше месяца начала")
    
    return cleaned_data
```

**Alternatives considered**:
- Валидация на уровне модели — отклонено: меньше гибкости в UX
- JavaScript валидация — отклонено: должна быть серверная валидация

**Source**: Django documentation, best practices для форм

---

### 4. django-autocomplete-light для Year/Month

**Decision**: Использовать стандартные Django form widgets с choices для Month, ForeignKey autocomplete для Year

**Rationale**:
- Month уже использует IntegerField с choices (MonthEnum) — достаточно стандартного select widget
- Year — ForeignKey модель, можно использовать autocomplete для удобства
- Для простой формы редактирования достаточно стандартных Django widgets

**Implementation pattern**:
```python
# Для Month: стандартный Select widget с choices
# Для Year: ModelSelect2 widget от django-autocomplete-light или стандартный Select
```

**Alternatives considered**:
- Полностью кастомные виджеты — отклонено: избыточная сложность
- Текстовые поля — отклонено: хуже UX, возможны ошибки ввода

**Source**: django-autocomplete-light документация, существующие формы проекта

---

## Technology Decisions Summary

| Component | Decision | Justification |
|-----------|----------|---------------|
| **Views** | Django CBV (DetailView, UpdateView) | Соответствует patterns проекта |
| **Forms** | Django ModelForm + bootstrap5 | Единый стиль, быстрая интеграция |
| **Validation** | Form clean() method | Серверная валидация, хороший UX |
| **Widgets** | Стандартные Django + autocomplete | Простота, соответствие проекту |
| **Templates** | Django templates + bootstrap5 | Соответствует конституции |

---

## Existing Project Patterns

### Models
- ReadingLog уже определён в `src/core/models.py`
- Связи: ForeignKey на BookEdition, Year
- Month использует IntegerField с choices

### Views (существующие)
- Проект использует CBV для CRUD операций
- Стандартные Django generic views

### Templates
- django-bootstrap5 для форм
- Наследование от базового template

### URLs
- Именованные URL patterns для reverse

---

## No Outstanding Clarifications

Все технические решения определены на основе:
1. Анализа существующего кода проекта
2. Django best practices
3. Конституции проекта

**Next Phase**: Phase 1 — Design & Contracts
