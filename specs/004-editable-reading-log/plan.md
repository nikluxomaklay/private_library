# Implementation Plan: Редактирование Reading Log

**Branch**: `004-editable-reading-log` | **Date**: 6 марта 2026 г. | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-editable-reading-log/spec.md`

## Summary

Добавление функциональности просмотра и редактирования записей Reading Log. Пользователь сможет переходить на детальную страницу Reading Log из различных мест интерфейса (Home, список Reading Log, страница Book Edition), просматривать информацию в режиме read-only и редактировать поля периода чтения (Year start, Month start, Year finish, Month finish) с валидацией дат.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Django 5.1.1, django-bootstrap5 24.3, django-autocomplete-light 3.12.1
**Storage**: PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server (веб-приложение)
**Project Type**: single (Django monolith)
**Performance Goals**: Стандартные требования для веб-приложения (время отклика < 200ms для CRUD операций)
**Constraints**: Существующая модель ReadingLog уже определена, изменения в модель не требуются
**Scale/Scope**: Частная библиотека, умеренная нагрузка

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **Model-First** | ✅ PASS | Модель ReadingLog уже существует, изменения не требуются |
| **Admin Interface** | ✅ PASS | Функционал будет доступен через Django admin |
| **Test-First** | ✅ PASS | Тесты будут написаны до реализации (TDD) |
| **Integration Testing** | ✅ PASS | Требуется тестирование связей между ReadingLog и BookEdition |
| **Observability** | ✅ PASS | Логирование операций редактирования |
| **Django-based** | ✅ PASS | Используются Django templates + django-bootstrap5 |
| **django-autocomplete-light** | ✅ PASS | Для селекторов Year/Month |
| **Russian Documentation** | ✅ PASS | Документация на русском языке |

**GATE RESULT**: ✅ PASS - все принципы соблюдены

### Post-Phase 1 Re-Check

| Principle | Status | Notes |
|-----------|--------|-------|
| **Model-First** | ✅ PASS | data-model.md подтверждает: модель не изменяется |
| **Admin Interface** | ✅ PASS | Views будут доступны через admin |
| **Test-First** | ✅ PASS | Задачи на тесты будут созданы через `/speckit.tasks` |
| **Integration Testing** | ✅ PASS | contracts/urls.md определяет тестирование views |
| **Observability** | ✅ PASS | quickstart.md включает логирование |
| **Django-based** | ✅ PASS | Все артефакты используют Django patterns |
| **django-autocomplete-light** | ✅ PASS | Формы используют стандартные Django widgets |
| **Russian Documentation** | ✅ PASS | Все документы на русском языке |

**GATE RESULT**: ✅ PASS - дизайн соответствует конституции

## Project Structure

### Documentation (this feature)

```text
specs/004-editable-reading-log/
├── plan.md              # Этот файл
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── models.py        # ReadingLog уже существует
│   ├── views.py         # Добавить: ReadingLogDetailView, ReadingLogUpdateView
│   ├── forms.py         # Добавить: ReadingLogForm
│   ├── urls.py          # Добавить маршруты для detail/update
│   └── templates/
│       └── core/
│           ├── readinglog_detail.html    # Новая: детальная страница
│           └── readinglog_form.html      # Новая: форма редактирования
└── tests/
    └── integration/
        └── test_readinglog_views.py      # Интеграционные тесты
```

**Structure Decision**: Single Django project. Существующая структура src/core/ расширяется новыми views, forms, templates для ReadingLog.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | Нет нарушений конституции | N/A |
