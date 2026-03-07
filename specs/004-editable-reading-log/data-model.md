# Data Model: Reading Log

**Feature**: 004-editable-reading-log  
**Date**: 6 марта 2026 г.

## Overview

Модель ReadingLog уже существует в проекте. Изменения в модель не требуются — функциональность редактирования реализуется на уровне views и forms.

## Existing Model

### ReadingLog

**Location**: `src/core/models.py`

```python
class ReadingLog(models.Model):
    book_edition = models.ForeignKey(
        'BookEdition',
        on_delete=models.PROTECT,
        related_name='reading_logs',
    )
    year_start = models.ForeignKey(
        'Year',
        on_delete=models.PROTECT,
        related_name='year_start',
        null=True, blank=True,
    )
    month_start = models.IntegerField(
        choices=MonthEnum.choices,
        null=True, blank=True,
        db_index=True
    )
    year_finish = models.ForeignKey(
        'Year',
        on_delete=models.PROTECT,
        related_name='year_finish',
        null=True, blank=True,
    )
    month_finish = models.IntegerField(
        choices=MonthEnum.choices,
        null=True, blank=True,
        db_index=True
    )
```

### Fields Description

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| **book_edition** | ForeignKey | Yes | No | Связь с BookEdition |
| **year_start** | ForeignKey | No | Yes | Год начала чтения |
| **month_start** | IntegerField | No | Yes | Месяц начала чтения (1-12) |
| **year_finish** | ForeignKey | No | Yes | Год окончания чтения |
| **month_finish** | IntegerField | No | Yes | Месяц окончания чтения (1-12) |

### Relationships

```
ReadingLog
├── book_edition → BookEdition (PROTECT)
├── year_start → Year (PROTECT)
├── year_finish → Year (PROTECT)
└── month_* → MonthEnum.choices (1-12)
```

### Business Rules

1. **Период может быть пустым**: Все поля year_start, month_start, year_finish, month_finish могут быть NULL
2. **Валидация дат**: Если указаны оба года, year_finish >= year_start
3. **Валидация месяцев**: Если год начала = году окончания, month_finish >= month_start
4. **Связь с книгой**: При удалении BookEdition нельзя удалить ReadingLog (PROTECT)

### Existing Properties

| Property | Returns | Description |
|----------|---------|-------------|
| **period** | str | Человекочитаемый период (напр. "2024 Январь - Март") |
| **period_for_template** | str (HTML) | Период с ссылками на Year для template |

## Form Model

### ReadingLogForm (to be created)

**Location**: `src/core/forms.py`

```python
class ReadingLogForm(forms.ModelForm):
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
        
        # Валидация: если оба года указаны, finish >= start
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

### Form Fields Configuration

| Field | Widget | Required | Help Text |
|-------|--------|----------|-----------|
| **year_start** | ModelSelect2 | No | Год начала чтения |
| **month_start** | Select | No | Месяц начала чтения |
| **year_finish** | ModelSelect2 | No | Год окончания чтения |
| **month_finish** | Select | No | Месяц окончания чтения |

## State Transitions

```
[Создание] → [Существующий ReadingLog] → [Редактирование] → [Обновлённый ReadingLog]
                                      ↓
                                 [Отмена] → [Существующий ReadingLog]
```

### Validation States

```
Form Data → [clean()] → {Valid?}
                        ├─ Yes → [save()] → [Redirect to Detail]
                        └─ No → [Render Form with Errors]
```

## No Database Migrations Required

✅ Модель ReadingLog уже существует  
✅ Все поля поддерживают null=True, blank=True  
✅ Валидация реализуется на уровне формы  
✅ Изменения требуются только в views, forms, templates
