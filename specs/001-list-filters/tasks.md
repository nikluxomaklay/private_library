# Implementation Tasks: List Filters

**Feature**: Filter functionality for 6 different list pages (Reading log, Authors, Books, Book editions, Publishers, Book series)
**Branch**: `001-list-filters` | **Date**: 11 февраля 2026 | **Spec**: [spec.md](spec.md)

## Implementation Strategy

This implementation will follow an incremental approach, starting with the highest priority user story (Reading Log filtering) and progressively adding filters for other entities. Each user story will be implemented as a complete, independently testable increment that adds value to the user.

## Dependencies

- User Story 1 (Reading Log) must be completed before User Stories 3 and 4 (Books and Book Editions) as they share some common components
- All foundational tasks must be completed before any user story implementation begins

## Parallel Execution Examples

Each user story can be implemented in parallel after foundational tasks are complete:
- User Story 2 (Authors) and User Story 5 (Publishers) can be implemented simultaneously
- User Story 3 (Books) and User Story 6 (Book Series) can be implemented simultaneously
- User Story 4 (Book Editions) depends on User Story 3 (Books) but can be parallelized with User Story 2 and User Story 5

---

## Phase 1: Setup

- [X] T001 Install django-filter dependency in requirements.txt
- [X] T002 Create filters.py file in books app to house all FilterSet classes
- [X] T003 Create base template for filter forms that matches existing content addition page styling

## Phase 2: Foundational Tasks

- [X] T010 Add database indexes to filtered fields as per data model specification
- [X] T011 Create base FilterSet class with common functionality for special character sanitization
- [X] T012 Implement character limit validation (255 chars) for all text-based filters
- [X] T013 Create common template components for filter forms with bootstrap styling
- [X] T014 Add clear filters functionality to reset all applied filters with single action

## Phase 3: User Story 1 - Filter Reading Log Entries (Priority: P1)

**Goal**: Enable users to filter their reading log by various criteria including publication year, month, book title, author name, publisher, and book series.

**Independent Test**: Can be fully tested by applying different combinations of filters on the reading log page and verifying that only matching entries are displayed, delivering the value of quickly finding specific books in the reading history.

- [X] T020 [US1] Create ReadingLogFilter class with year 'from' and 'to' selectors (FR-001)
- [X] T021 [US1] Add month 'from' and 'to' selectors to ReadingLogFilter (FR-002)
- [X] T022 [US1] Implement combined year+month 'from' and 'to' selectors in ReadingLogFilter (FR-003)
- [X] T023 [US1] Add book title search by substring to ReadingLogFilter (FR-004)
- [X] T024 [US1] Add author name search by substring to ReadingLogFilter (FR-005)
- [X] T025 [US1] Add publisher name search by substring to ReadingLogFilter (FR-006)
- [X] T026 [US1] Add publication year exact match filter to ReadingLogFilter (FR-007)
- [X] T027 [US1] Add book series name search by substring to ReadingLogFilter (FR-008)
- [X] T028 [US1] Create ReadingLogListView using django-filter's FilterView (FR-001-008)
- [X] T029 [US1] Update reading_log_list.html template to include filter form with proper styling (FR-019)
- [X] T030 [US1] Add clear filters button to reading log filter form (FR-020)
- [X] T031 [US1] Implement empty results display for reading log (FR-022, FR-027)
- [X] T032 [US1] Test reading log filtering with various combinations of criteria (Acceptance Scenario 1-3)

## Phase 4: User Story 2 - Filter Authors List (Priority: P2)

**Goal**: Enable users to filter the authors list by name to quickly find specific authors in the database.

**Independent Test**: Can be fully tested by entering different substrings in the author name filter and verifying that only matching authors are displayed, delivering the value of quickly finding specific authors.

- [X] T040 [US2] Create AuthorFilter class with author name search by substring (FR-009)
- [X] T041 [US2] Create AuthorListView using django-filter's FilterView (FR-009)
- [X] T042 [US2] Update author_list.html template to include filter form with proper styling (FR-019)
- [X] T043 [US2] Add clear filters button to authors filter form (FR-020)
- [X] T044 [US2] Implement empty results display for authors list (FR-022, FR-027)
- [X] T045 [US2] Test author filtering with various name substrings (Acceptance Scenario 1)

## Phase 5: User Story 3 - Filter Books List (Priority: P2)

**Goal**: Enable users to filter the books list by title and author name to quickly find specific books in the database.

**Independent Test**: Can be fully tested by entering different substrings in the book title and author name filters and verifying that only matching books are displayed, delivering the value of quickly finding specific books.

- [X] T050 [US3] Create BookFilter class with book title search by substring (FR-010)
- [X] T051 [US3] Add author name search by substring to BookFilter using django-autocomplete-light (FR-011)
- [X] T052 [US3] Create BookListView using django-filter's FilterView (FR-010-011)
- [X] T053 [US3] Update book_list.html template to include filter form with proper styling (FR-019)
- [X] T054 [US3] Add clear filters button to books filter form (FR-020)
- [X] T055 [US3] Implement empty results display for books list (FR-022, FR-027)
- [X] T056 [US3] Test book filtering with various title and author name substrings (Acceptance Scenario 1-2)

## Phase 6: User Story 4 - Filter Book Editions List (Priority: P3)

**Goal**: Enable users to filter the book editions list by title, author, publisher, publication year, and book series to find specific editions.

**Independent Test**: Can be fully tested by applying different combinations of filters on the book editions page and verifying that only matching editions are displayed, delivering the value of quickly finding specific book editions.

- [X] T060 [US4] Create BookEditionFilter class with book title search by substring (FR-012)
- [X] T061 [US4] Add author name search by substring to BookEditionFilter using django-autocomplete-light (FR-013)
- [X] T062 [US4] Add publisher name search by substring to BookEditionFilter (FR-014)
- [X] T063 [US4] Add publication year exact match filter to BookEditionFilter (FR-015)
- [X] T064 [US4] Add book series name search by substring to BookEditionFilter (FR-016)
- [X] T065 [US4] Create BookEditionListView using django-filter's FilterView (FR-012-016)
- [X] T066 [US4] Update book_edition_list.html template to include filter form with proper styling (FR-019)
- [X] T067 [US4] Add clear filters button to book editions filter form (FR-020)
- [X] T068 [US4] Implement empty results display for book editions (FR-022, FR-027)
- [X] T069 [US4] Test book edition filtering with various combinations of criteria (Acceptance Scenario 1-2)

## Phase 7: User Story 5 - Filter Publishers List (Priority: P3)

**Goal**: Enable users to filter the publishers list by name to quickly find specific publishers in the database.

**Independent Test**: Can be fully tested by entering different substrings in the publisher name filter and verifying that only matching publishers are displayed, delivering the value of quickly finding specific publishers.

- [X] T070 [US5] Create PublisherFilter class with publisher name search by substring (FR-017)
- [X] T071 [US5] Create PublisherListView using django-filter's FilterView (FR-017)
- [X] T072 [US5] Update publisher_list.html template to include filter form with proper styling (FR-019)
- [X] T073 [US5] Add clear filters button to publishers filter form (FR-020)
- [X] T074 [US5] Implement empty results display for publishers list (FR-022, FR-027)
- [X] T075 [US5] Test publisher filtering with various name substrings (Acceptance Scenario 1)

## Phase 8: User Story 6 - Filter Book Series List (Priority: P3)

**Goal**: Enable users to filter the book series list by name to quickly find specific book series in the database.

**Independent Test**: Can be fully tested by entering different substrings in the book series name filter and verifying that only matching series are displayed, delivering the value of quickly finding specific book series.

- [X] T080 [US6] Create BookSeriesFilter class with book series name search by substring (FR-018)
- [X] T081 [US6] Create BookSeriesListView using django-filter's FilterView (FR-018)
- [X] T082 [US6] Update book_series_list.html template to include filter form with proper styling (FR-019)
- [X] T083 [US6] Add clear filters button to book series filter form (FR-020)
- [X] T084 [US6] Implement empty results display for book series (FR-022, FR-027)
- [X] T085 [US6] Test book series filtering with various name substrings (Acceptance Scenario 1)

## Phase 9: Polish & Cross-Cutting Concerns

- [X] T090 Add special character handling tests to ensure sanitization works properly (FR-023)
- [X] T091 Verify all filter inputs maintain same styling as existing content addition pages (FR-019)
- [X] T092 Ensure anonymous access works for all filter functionality (FR-024)
- [X] T093 Verify partial matching works for all 'поиск по подстроке' fields (FR-025)
- [X] T094 Test character limits (255 chars) on all text-based filters (FR-026)
- [X] T095 Performance test: ensure filter operations complete within 2 seconds (SC-001, SC-002)
- [X] T096 Verify 95% of users can successfully apply filters and find desired entries (SC-003)
- [X] T097 Test clear filters functionality across all pages (SC-005)
- [X] T098 Verify empty results display works appropriately (SC-006)
- [X] T099 Update documentation with usage instructions for the new filter functionality