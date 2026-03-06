# Tasks: Редактирование Reading Log

**Input**: Design documents from `/specs/004-editable-reading-log/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification or if TDD approach is desired.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure as per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure verification

- [ ] T001 Verify project structure matches plan.md (src/core/ directory exists)
- [ ] T002 [P] Verify Django dependencies installed (requirements.txt: django-bootstrap5, django-autocomplete-light)
- [ ] T003 [P] Verify PostgreSQL database connection configured (default.config.yml)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Verify ReadingLog model exists in src/core/models.py
- [ ] T005 [P] Verify Year model exists in src/core/models.py
- [ ] T006 [P] Verify MonthEnum exists in src/core/enums.py
- [ ] T007 Verify base template exists: src/core/templates/base.html
- [ ] T008 Verify URL configuration exists: src/core/urls.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Просмотр детальной информации о Reading log (Priority: P1) 🎯 MVP

**Goal**: Создание детальной страницы просмотра ReadingLog с возможностью перехода из различных мест интерфейса

**Independent Test**: Пользователь может перейти на детальную страницу ReadingLog из Home, списка ReadingLog или страницы BookEdition и увидеть всю информацию в режиме read-only

### Implementation for User Story 1

- [ ] T009 [P] [US1] Создать ReadingLogDetailView в src/core/views.py
- [ ] T010 [P] [US1] Создать template детальной страницы: src/core/templates/core/readinglog_detail.html
- [ ] T011 [P] [US1] Добавить URL маршрут для readinglog_detail в src/core/urls.py
- [ ] T012 [US1] Добавить кнопку "Назад" в src/core/templates/core/readinglog_detail.html
- [ ] T013 [US1] Обновить Home template: заменить период ReadingLog на ссылку на детальную страницу (src/core/templates/core/home.html)
- [ ] T014 [US1] Обновить BookEdition detail template: заменить ссылки на год на ссылку на ReadingLog detail (src/core/templates/core/bookedition_detail.html)
- [ ] T015 [US1] Добавить логирование для операций просмотра ReadingLog (src/core/views.py)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Редактирование Reading log (Priority: P2)

**Goal**: Создание страницы редактирования ReadingLog с валидацией дат

**Independent Test**: Пользователь может перейти с детальной страницы на страницу редактирования, изменить поля Year start, Month start, Year finish, Month finish и сохранить изменения

### Implementation for User Story 2

- [ ] T016 [P] [US2] Создать ReadingLogForm в src/core/forms.py с валидацией дат
- [ ] T017 [P] [US2] Создать ReadingLogUpdateView в src/core/views.py
- [ ] T018 [P] [US2] Создать template формы редактирования: src/core/templates/core/readinglog_form.html
- [ ] T019 [P] [US2] Добавить URL маршрут для readinglog_update в src/core/urls.py
- [ ] T020 [US2] Добавить кнопку "Update" в src/core/templates/core/readinglog_detail.html в блоке действий
- [ ] T021 [US2] Добавить кнопку "Отмена" в src/core/templates/core/readinglog_form.html
- [ ] T022 [US2] Реализовать перенаправление на детальную страницу после сохранения (src/core/views.py: get_success_url)
- [ ] T023 [US2] Реализовать перенаправление на детальную страницу при отмене (src/core/templates/core/readinglog_form.html)
- [ ] T024 [US2] Добавить обработку ошибок валидации формы (src/core/templates/core/readinglog_form.html)
- [ ] T025 [US2] Добавить логирование для операций редактирования ReadingLog (src/core/views.py)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T026 [P] Проверка маршрутов: python src/manage.py show_urls | grep readinglog
- [ ] T027 [P] Ручное тестирование по сценариям из quickstart.md (src/specs/004-editable-reading-log/quickstart.md)
- [ ] T028 [P] Проверка валидации: ввести некорректные даты, убедиться в появлении ошибки (src/core/forms.py: clean method)
- [ ] T029 Проверка отображения пустых значений полей в src/core/templates/core/readinglog_detail.html
- [ ] T030 [P] Финальная проверка: запуск сервера и тестирование полного цикла (python src/manage.py runserver)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 (кнопка Update на детальной странице)

### Within Each User Story

**User Story 1**:
- Views и templates могут создаваться параллельно
- URL маршруты после views
- Обновление существующих templates после создания детальной страницы

**User Story 2**:
- Форма должна быть создана до views
- Views должны быть созданы до templates
- Кнопки добавляются после создания templates

### Parallel Opportunities

- **Phase 1**: T002, T003 могут выполняться параллельно
- **Phase 2**: T004, T005, T006 могут выполняться параллельно
- **Phase 3 (US1)**: T009, T010, T011 могут выполняться параллельно (разные файлы)
- **Phase 4 (US2)**: T016, T017, T018, T019 могут выполняться параллельно (разные файлы)

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1:
# Developer A: T009 - Create ReadingLogDetailView in src/core/views.py
# Developer B: T010 - Create readinglog_detail.html template
# Developer C: T011 - Add URL route to src/core/urls.py
```

---

## Parallel Example: User Story 2

```bash
# Launch all parallel tasks for User Story 2:
# Developer A: T016 - Create ReadingLogForm in src/core/forms.py
# Developer B: T017 - Create ReadingLogUpdateView in src/core/views.py
# Developer C: T018 - Create readinglog_form.html template
# Developer D: T019 - Add URL route to src/core/urls.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: 
   - Проверить переход на детальную страницу из Home
   - Проверить переход из BookEdition detail
   - Проверить отображение всех полей в read-only режиме
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (views, templates, URLs)
   - Developer B: User Story 2 (form, update view, templates) - может начаться после US1
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1 | Setup | 3 |
| Phase 2 | Foundational | 5 |
| Phase 3 | User Story 1 (P1) | 7 |
| Phase 4 | User Story 2 (P2) | 10 |
| Phase 5 | Polish | 5 |
| **Total** | | **30** |

### Task Count per User Story

- **User Story 1**: 7 задач (T009-T015)
- **User Story 2**: 10 задач (T016-T025)

### Independent Test Criteria

- **User Story 1**: Переход на детальную страницу из 3 источников, отображение read-only
- **User Story 2**: Редактирование 4 полей, валидация дат, сохранение, отмена

### MVP Scope

**MVP = User Story 1 Only**:
- Детальная страница ReadingLog (T009-T011)
- Кнопка "Назад" (T012)
- Ссылки на детальную страницу из Home и BookEdition (T013-T014)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Model ReadingLog уже существует - миграции не требуются
- Валидация дат реализуется на уровне формы (clean method)
