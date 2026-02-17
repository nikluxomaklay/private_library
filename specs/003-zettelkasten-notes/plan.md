# Implementation Plan: Zettelkasten Notes System

**Branch**: `003-zettelkasten-notes` | **Date**: 17 февраля 2026 г. | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-zettelkasten-notes/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Реализация системы заметок Zettelkasten в рамках существующего Django-приложения частной библиотеки. Система позволяет создавать иерархические заметки, связывать их с книжными изданиями, добавлять ключевые слова и управлять связями между заметками. Модели данных уже реализованы, требуется реализовать views, forms, templates и URLs для CRUD операций.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Django 4.x, django-bootstrap5, django-autocomplete-light
**Storage**: PostgreSQL (существующая БД библиотеки)
**Testing**: pytest, pytest-django
**Target Platform**: Веб-приложение (серверная рендеринг)
**Project Type**: Web application (существующая структура: core + front приложения)
**Performance Goals**: Стандартные для Django-приложения требования
**Constraints**: Реализация в рамках существующих app (core, front), без создания новых
**Scale/Scope**: Локальное использование, стандартные требования к производительности

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (before Phase 0)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Model-First | ✅ PASS | Модели Note, NoteToBookEdition, KeyWord уже реализованы |
| II. Admin Interface | ✅ N/A | Не требуется в рамках этой функции |
| III. Test-First (NON-NEGOTIABLE) | ✅ READY | TDD будет применён при реализации |
| IV. Integration Testing | ✅ READY | Тесты для связей между моделями запланированы |
| V. Observability | ✅ READY | Логирование и отладка предусмотрены |

**Gate Result**: PASS - все принципы соблюдены или будут реализованы

### Re-Check (after Phase 1)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Model-First | ✅ PASS | Модели документированы в data-model.md |
| II. Admin Interface | ✅ N/A | Не требуется в рамках этой функции |
| III. Test-First | ✅ READY | Testing checklist в quickstart.md |
| IV. Integration Testing | ✅ READY | Контракты для integration tests в api-contracts.md |
| V. Observability | ✅ READY | Quickstart включает debugging guidance |

**Gate Result**: PASS - дизайн завершён, готов к Phase 2

## Project Structure

### Documentation (this feature)

```text
specs/003-zettelkasten-notes/
├── plan.md              # Этот файл
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
# Backend (Django)
core/
├── models/
│   ├── note.py          # Note модель
│   ├── note_to_book.py  # NoteToBookEdition связь
│   └── keyword.py       # KeyWord модель

front/
├── views/
│   └── notes.py         # Views для CRUD операций
├── forms/
│   └── notes.py         # Формы для заметок
├── urls/
│   └── notes.py         # URL маршруты
├── templates/
│   └── front/notes/
│       ├── list.html          # Список заметок
│       ├── detail.html        # Детальная страница
│       ├── form.html          # Форма создания/редактирования
│       └── _note_tree.html    # partial для иерархии
└── static/
    └── front/
        └── js/
            └── notes.js       # JavaScript для динамических элементов

tests/
├── unit/
│   ├── test_note_model.py
│   ├── test_note_forms.py
│   └── test_note_views.py
└── integration/
    ├── test_note_hierarchy.py
    └── test_note_book_relations.py
```

**Structure Decision**: Используется существующая структура проекта с разделением на core (модели) и front (views, forms, templates, static). Новые app не создаются согласно требованиям.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Нет нарушений | - | - |

---

## Phase 0: Research & Discovery

### Research Tasks

1. **Изучить существующую реализацию селекторов с live-поиском** на примере поля Publisher
   - Файл: `front/forms/book_edition.py` (или аналогичный)
   - Цель: Понять паттерн реализации django-autocomplete-light
   - Outcome: Документированный паттерн для reuse

2. **Изучить существующие views для CRUD операций** с книжными изданиями
   - Файлы: `front/views/book_edition.py`, `front/urls/book_edition.py`
   - Цель: Понять структуру URL, naming conventions, паттерны views
   - Outcome: Список URL паттернов для заметок

3. **Изучить реализацию пагинации** в существующих списках
   - Файлы: существующие list views
   - Цель: Определить стандартный лимит пагинации
   - Outcome: Числовое значение для лимита пагинации заметок

4. **Изучить структуру templates** существующих страниц
   - Файлы: `front/templates/front/`
   - Цель: Понять структуру шаблонов, использование bootstrap5
   - Outcome: Структура шаблонов для заметок

5. **Исследовать существующие M2M связи** с additional info
   - Файлы: модели с промежуточными таблицами
   - Цель: Понять паттерны работы с NoteToBookEdition
   - Outcome: Паттерн для inline-форм с дополнительными данными

### Research Output

✅ Завершено: [`research.md`](research.md)

**Key Findings**:
- Pagination default: 25 items
- Autocomplete pattern: django-autocomplete-light (Select2)
- Inline formset pattern для NoteToBookEdition
- Class-based views для CRUD операций

---

## Phase 1: Design & Contracts

✅ Завершено

### Data Model

✅ Завершено: [`data-model.md`](data-model.md)

**Entities**:
- Note (основная модель, иерархическая структура)
- NoteToBookEdition (промежуточная модель M2M)
- KeyWord (ключевые слова)

**Validation Rules**:
- Topic required, max 255 chars
- Circular dependency blocking
- Empty inline elements ignored

### API Contracts

✅ Завершено: [`contracts/api-contracts.md`](contracts/api-contracts.md)

**URL Patterns**:
- `/note/` - список
- `/note/new/` - создание
- `/note/<int:pk>/` - детальная
- `/note/<int:pk>/update/` - редактирование
- `/note/<int:pk>/delete/` - удаление
- `/note/autocomplete/` - autocomplete для parent
- `/keyword/autocomplete/` - autocomplete для keywords

### Quickstart Guide

✅ Завершено: [`quickstart.md`](quickstart.md)

**Содержание**:
- Структура проекта
- Основные команды
- Порядок реализации
- Ключевые паттерны кода
- User scenarios
- Testing checklist

### Agent Context Update

✅ Завершено: Qwen agent context updated

**Updated**:
- Language: Python 3.11
- Framework: Django 4.x, django-bootstrap5, django-autocomplete-light
- Database: PostgreSQL

---

## Phase 2: Implementation Tasks

См. [`tasks.md`](tasks.md) (создаётся командой `/speckit.tasks`)
