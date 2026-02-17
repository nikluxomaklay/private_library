# Tasks: Zettelkasten Notes System

**Input**: Design documents from `/specs/003-zettelkasten-notes/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD mandatory per constitution - tests written → User approved → Tests fail → Then implement

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project structure**: `src/core/`, `src/front/`, `src/tests/`
- **Models**: `src/core/models.py` (уже реализованы)
- **Views**: `src/front/views/`
- **Forms**: `src/front/forms/`
- **Templates**: `src/templates/front/notes/`
- **Tests**: `src/core/tests/`, `src/front/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure verification

- [ ] T001 Verify project structure: src/core/, src/front/, src/templates/
- [ ] T002 [P] Verify dependencies: django-autocomplete-light, django-bootstrap5, django-filter
- [ ] T003 [P] Verify PostgreSQL database connection and existing migrations

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create NoteFilter in src/core/filters.py (django-filter для заметок)
- [ ] T005 [P] Create NoteForm in src/front/forms/notes.py (базовая форма)
- [ ] T006 [P] Create NoteToBookEditionFormSet в src/front/forms/notes.py (inline formset)
- [ ] T007 [P] Create autocomplete views в src/front/views/notes.py (NoteAutocompleteView, KeyWordAutocompleteView)
- [ ] T008 [P] Add URL patterns для autocomplete в src/front/urls.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Просмотр списка заметок (Priority: P1) 🎯 MVP

**Goal**: Реализовать боковое меню с пунктом "Notes" и страницу списка заметок с иерархией и пагинацией

**Independent Test**: Пользователь может перейти в раздел Notes из бокового меню и увидеть список всех заметок с правильной иерархией и пагинацией

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Integration test: note list page renders with hierarchy in src/front/tests/test_note_list.py::test_note_list_hierarchy
- [ ] T010 [P] [US1] Integration test: pagination applies to top-level notes only in src/front/tests/test_note_list.py::test_note_list_pagination
- [ ] T011 [P] [US1] Template test: note list displays index and topic in src/front/tests/test_note_templates.py::test_note_list_displays

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create NoteListView в src/front/views/notes.py (PaginationPageSizeMixin, FilterView)
- [ ] T013 [P] [US1] Create template src/templates/front/notes/note_list.html (иерархия с отступами)
- [ ] T014 [P] [US1] Create partial template src/templates/front/notes/_note_tree.html (recursive rendering)
- [ ] T015 [US1] Add URL pattern 'note' в src/front/urls.py
- [ ] T016 [US1] Add "Notes" пункт в боковое меню в src/templates/base_layout.html
- [ ] T017 [US1] Implement hierarchical queryset с prefetch_related для дочерних заметок
- [ ] T018 [US1] Add context processors для передачи иерархии в template

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Просмотр детальной страницы заметки (Priority: P1)

**Goal**: Реализовать детальную страницу заметки со всей информацией

**Independent Test**: Пользователь может кликнуть на индекс заметки в списке и увидеть детальную страницу со всей информацией

### Tests for User Story 2 ⚠️

- [ ] T019 [P] [US2] Integration test: note detail page displays all fields in src/front/tests/test_note_detail.py::test_note_detail_displays_all
- [ ] T020 [P] [US2] Integration test: note detail shows related book editions with info in src/front/tests/test_note_detail.py::test_note_detail_book_editions

### Implementation for User Story 2

- [ ] T021 [P] [US2] Create NoteDetailView в src/front/views/notes.py (DetailView с select_related/prefetch_related)
- [ ] T022 [P] [US2] Create template src/templates/front/notes/note_detail.html
- [ ] T023 [US2] Add URL pattern 'note_detail' в src/front/urls.py
- [ ] T024 [US2] Implement index link в note_list.html → note_detail
- [ ] T025 [US2] Add display logic для parent, keywords, related_notes, book_editions с additional_info
- [ ] T026 [US2] Add display logic для created_at/updated_at в одной строке

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Просмотр связанных заметок на странице книжного издания (Priority: P2)

**Goal**: Отображать связанные заметки на детальной странице книжного издания

**Independent Test**: На странице детального просмотра книжного издания отображается блок со связанными заметками в иерархическом виде

### Tests for User Story 3 ⚠️

- [ ] T027 [P] [US3] Integration test: book edition detail shows related notes in src/front/tests/test_book_edition_detail.py::test_book_edition_shows_notes
- [ ] T028 [P] [US3] Integration test: related notes display hierarchy in src/front/tests/test_book_edition_detail.py::test_book_edition_notes_hierarchy

### Implementation for User Story 3

- [ ] T029 [P] [US3] Add related_notes queryset property в BookEdition model или view context
- [ ] T030 [US3] Update template src/templates/book_edition/book_edition_detail.html (добавить блок с заметками)
- [ ] T031 [US3] Create partial template src/templates/front/notes/_note_tree_readonly.html (для отображения в book edition)
- [ ] T032 [US3] Implement hierarchical display с отступами для связанных заметок

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Добавление заметки со страницы списка заметок (Priority: P2)

**Goal**: Реализовать создание новой заметки через кнопку "New note" на странице списка

**Independent Test**: Пользователь может нажать кнопку "New note" на странице списка, заполнить форму и создать новую заметку

### Tests for User Story 4 ⚠️

- [ ] T033 [P] [US4] Integration test: create note with topic only in src/front/tests/test_note_create.py::test_create_note_minimal
- [ ] T034 [P] [US4] Integration test: create note with book editions inline in src/front/tests/test_note_create.py::test_create_note_with_books
- [ ] T035 [P] [US4] Validation test: note without topic fails in src/front/tests/test_note_forms.py::test_note_form_requires_topic
- [ ] T036 [P] [US4] Validation test: circular dependency blocked in src/front/tests/test_note_forms.py::test_circular_dependency_blocked

### Implementation for User Story 4

- [ ] T037 [P] [US4] Create NoteNewView (CreateView) в src/front/views/notes.py
- [ ] T038 [P] [US4] Create template src/templates/front/notes/note_new.html
- [ ] T039 [US4] Add URL pattern 'note_new' в src/front/urls.py
- [ ] T040 [US4] Add "New note" кнопку в note_list.html
- [ ] T041 [US4] Implement form validation для topic (required, max 255)
- [ ] T042 [US4] Implement inline formset handling для NoteToBookEdition
- [ ] T043 [US4] Implement conditional logic: additional_info disabled без book_edition
- [ ] T044 [US4] Implement empty element filtering (игнорировать без book_edition)
- [ ] T045 [US4] Implement circular dependency check при сохранении
- [ ] T046 [US4] Add success message после создания
- [ ] T047 [US4] Add redirect to note_detail после успешного создания

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Добавление заметки со страницы книжного издания (Priority: P3)

**Goal**: Реализовать создание заметки с предзаполненным книжным изданием

**Independent Test**: На странице книжного издания есть кнопка "New note", при нажатии на которую форма создания содержит уже выбранное текущее издание

### Tests for User Story 5 ⚠️

- [ ] T048 [P] [US5] Integration test: create note from book edition with pre-filled field in src/front/tests/test_note_create.py::test_create_note_from_book_edition

### Implementation for User Story 5

- [ ] T049 [P] [US5] Add "New note" кнопку в src/templates/book_edition/book_edition_detail.html
- [ ] T050 [US5] Update NoteNewView для обработки initial['book_editions'] из query params
- [ ] T051 [US5] Add URL parameter passing из book_edition_detail → note_new

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Добавление заметки со страницы другой заметки (Priority: P3)

**Goal**: Реализовать создание заметки с предзаполненными полями из другой заметки

**Independent Test**: На странице заметки есть кнопка "New note", при нажатии на которую форма создания содержит данные текущей заметки в соответствующих полях (кроме Тема и Текст)

### Tests for User Story 6 ⚠️

- [ ] T052 [P] [US6] Integration test: create note from note with pre-filled parent, books, keywords in src/front/tests/test_note_create.py::test_create_note_from_note

### Implementation for User Story 6

- [ ] T053 [P] [US6] Add "New note" кнопку в src/templates/front/notes/note_detail.html
- [ ] T054 [US6] Update NoteNewView для обработки initial из parent note (parent, book_editions, keywords)
- [ ] T055 [US6] Ensure topic and text fields remain empty при pre-fill из другой заметки
- [ ] T056 [US6] Add URL parameter passing из note_detail → note_new

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 9: User Story 7 - Изменение заметки (Priority: P2)

**Goal**: Реализовать редактирование существующей заметки

**Independent Test**: Пользователь может открыть существующую заметку на редактирование, изменить поля и сохранить изменения

### Tests for User Story 7 ⚠️

- [ ] T057 [P] [US7] Integration test: update note topic in src/front/tests/test_note_update.py::test_update_note_topic
- [ ] T058 [P] [US7] Integration test: update note book editions inline in src/front/tests/test_note_update.py::test_update_note_books
- [ ] T059 [P] [US7] Validation test: update with circular dependency blocked in src/front/tests/test_note_update.py::test_update_circular_blocked

### Implementation for User Story 7

- [ ] T060 [P] [US7] Create NoteUpdateView (UpdateView) в src/front/views/notes.py
- [ ] T061 [P] [US7] Create template src/templates/front/notes/note_update.html
- [ ] T062 [US7] Add URL pattern 'note_update' в src/front/urls.py
- [ ] T063 [US7] Add "Edit" кнопку в note_detail.html
- [ ] T064 [US7] Implement form pre-population с текущими данными
- [ ] T065 [US7] Implement inline formset с existing instances
- [ ] T066 [US7] Implement circular dependency check при обновлении parent
- [ ] T067 [US7] Add success message после обновления
- [ ] T068 [US7] Add redirect to note_detail после успешного обновления

**Checkpoint**: At this point, User Stories 1-7 should all work independently

---

## Phase 10: User Story 8 - Удаление заметки (Priority: P2)

**Goal**: Реализовать удаление заметки с защитой от удаления родительских заметок

**Independent Test**: Пользователь может удалить заметку без дочерних; попытка удалить заметку с дочерними блокируется

### Tests for User Story 8 ⚠️

- [ ] T069 [P] [US8] Integration test: delete note without children in src/front/tests/test_note_delete.py::test_delete_note_without_children
- [ ] T070 [P] [US8] Validation test: delete note with children blocked in src/front/tests/test_note_delete.py::test_delete_note_with_children_blocked

### Implementation for User Story 8

- [ ] T071 [P] [US8] Create NoteDeleteView (DeleteView) в src/front/views/notes.py
- [ ] T072 [P] [US8] Create template src/templates/front/notes/note_delete.html
- [ ] T073 [US8] Add URL pattern 'note_delete' в src/front/urls.py
- [ ] T074 [US8] Add "Delete" кнопку в note_detail.html
- [ ] T075 [US8] Implement check for children перед удалением
- [ ] T076 [US8] Implement error message при попытке удаления с дочерними
- [ ] T077 [US8] Add redirect to note_list после успешного удаления

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T078 [P] Add JavaScript для dynamic inline formset behavior в src/static/front/js/notes.js
- [ ] T079 [P] Add JavaScript для conditional additional_info field disabling
- [ ] T080 [P] Add CSS styles для иерархических отступов в src/static/front/css/notes.css
- [ ] T081 Documentation: Update README.md с описанием системы заметок
- [ ] T082 Code cleanup and refactoring
- [ ] T083 Run quickstart.md validation checklist
- [ ] T084 [P] Run all tests: pytest src/core/tests/ src/front/tests/
- [ ] T085 Security hardening: CSRF, XSS protection check

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Список заметок - может начинаться после Foundational
- **User Story 2 (P1)**: Детальная страница - может начинаться после Foundational, зависит от US1 только для навигации
- **User Story 3 (P2)**: Заметки на странице издания - может начинаться после Foundational
- **User Story 4 (P2)**: Создание заметки - может начинаться после Foundational
- **User Story 5 (P3)**: Создание из издания - зависит от US4 + book edition detail
- **User Story 6 (P3)**: Создание из заметки - зависит от US4 + note detail
- **User Story 7 (P2)**: Редактирование - может начинаться после Foundational
- **User Story 8 (P2)**: Удаление - может начинаться после Foundational

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD per constitution)
- Views before templates
- Forms before views
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T002, T003 могут выполняться параллельно
- **Phase 2 (Foundational)**: T004-T008 могут выполняться параллельно (разные файлы)
- **Phase 3+ (User Stories)**: После завершения Phase 2, разные разработчики могут работать на разных user stories
- **Tests within a story**: Все тесты для story могут писаться параллельно
- **Models within a story**: Не применимо (модели уже реализованы)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Integration test: note list page renders with hierarchy"
Task: "Integration test: pagination applies to top-level notes only"
Task: "Template test: note list displays index and topic"

# Launch implementation for User Story 1:
Task: "Create NoteListView" (views/notes.py)
Task: "Create template note_list.html" (templates/front/notes/)
Task: "Create partial template _note_tree.html" (templates/front/notes/)
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (список заметок)
4. Complete Phase 4: User Story 2 (детальная страница)
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (список) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (детальная) → Test independently → Deploy/Demo
4. Add User Story 4 (создание) → Test independently → Deploy/Demo
5. Add User Story 7 (редактирование) → Test independently → Deploy/Demo
6. Add User Story 8 (удаление) → Test independently → Deploy/Demo
7. Add User Story 3 (заметки на изданиях) → Test independently → Deploy/Demo
8. Add User Story 5, 6 (предзаполнение) → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (список)
   - Developer B: User Story 4 (создание)
   - Developer C: User Story 7 (редактирование)
3. Stories complete and integrate independently

---

## Notes

- **[P]** tasks = different files, no dependencies within phase
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD mandatory**: Verify tests fail before implementing (Constitution Principle III)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Модели Note, NoteToBookEdition, KeyWord уже реализованы в src/core/models.py
- Миграция уже существует
- Использовать django-autocomplete-light для селекторов (паттерн: PublisherAutocompleteView)
- Использовать PaginationPageSizeMixin для пагинации (default: 25)
- Использовать inline formset для NoteToBookEdition
