# Tasks: Book Edition Type

**Feature**: Book Edition Type
**Branch**: `002-book-edition-type`
**Generated**: 11 февраля 2026
**Input**: `/specs/002-book-edition-type/spec.md`, `/specs/002-book-edition-type/plan.md`

## Implementation Strategy

**MVP Scope**: User Story 1 (Add book edition type during creation) - This delivers the core functionality allowing users to specify book edition types during creation.

**Incremental Delivery**:
- Phase 1: Setup and foundational work
- Phase 2: Core model functionality (US1)
- Phase 3: UI for creation (US1)
- Phase 4: Display in list view (US2)
- Phase 5: Display in detail view (US3)

## Phase 1: Setup

- [ ] T001 Create apps/books directory if it doesn't exist
- [ ] T002 Verify Django project structure exists
- [ ] T003 Create initial migration for edition type field

## Phase 2: Foundational

- [ ] T004 [P] Update BookEdition model with edition_type CharField
- [ ] T005 [P] Create and run migration for edition_type field
- [ ] T006 [P] Define constants for edition types in models.py

## Phase 3: User Story 1 - Add book edition type during creation (Priority: P1)

**Story Goal**: As a system user, I want to specify the type of book edition when adding a new book edition.

**Independent Test**: Can be fully tested by creating a new book edition with a specific type and verifying it's saved correctly, delivering the value of organized book formats.

**Acceptance Scenarios**:
1. Given user is on the book edition creation page, When user selects a book edition type and submits the form, Then the book edition is saved with the selected type
2. Given user is on the book edition creation page, When user does not select a book edition type, Then the system defaults to 'Paper Book' type

- [ ] T007 [US1] Update BookEditionForm to include edition_type dropdown
- [ ] T008 [US1] Add validation to ensure edition_type is required during creation
- [ ] T009 [US1] Set default value to 'PAPER_BOOK' in form
- [ ] T010 [US1] Update interface to show edition_type field in creation form
- [ ] T011 [US1] Make edition_type field read-only in change form (immutability)
- [ ] T012 [US1] Test creating book edition with specific type
- [ ] T013 [US1] Test creating book edition without specifying type (should default)

## Phase 4: User Story 2 - View book edition type in list view (Priority: P2)

**Story Goal**: As a system user, I want to see the book edition type displayed as an icon in the list view so I can quickly identify the format of each book.

**Independent Test**: Can be tested by viewing the book edition list and verifying icons are displayed correctly for each type, delivering the value of quick visual scanning.

**Acceptance Scenarios**:
1. Given user is viewing the book edition list, When book editions are displayed, Then each entry shows the appropriate icon representing its type (📖 for Paper Book, 📄 for E-book, 🎙️ for Audiobook, 🌐 for Web Page)

- [ ] T014 [US2] Update book list template to display edition type as Unicode icon
- [ ] T015 [US2] Create helper function to map edition type to Unicode icon
- [ ] T016 [US2] Test that icons appear correctly in list view for each type
- [ ] T017 [US2] Verify styling is consistent with existing elements

## Phase 5: User Story 3 - View book edition type in detail view (Priority: P3)

**Story Goal**: As a system user, I want to see the book edition type displayed as text on the detail page so I can clearly understand the format of the book.

**Independent Test**: Can be tested by viewing a book edition detail page and verifying the type is displayed as readable text, delivering the value of clear format identification.

**Acceptance Scenarios**:
1. Given user is viewing a book edition detail page, When the page loads, Then the book edition type is displayed as readable text alongside other book properties

- [ ] T018 [US3] Update book detail template to display edition type as text
- [ ] T019 [US3] Test that edition type appears correctly in detail view
- [ ] T020 [US3] Verify styling is consistent with other property displays

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T021 Update documentation to reflect new functionality
- [ ] T022 Run all tests to ensure no regressions
- [ ] T023 Verify interface works correctly with new field
- [ ] T024 Perform manual testing of all functionality
- [ ] T025 Clean up any temporary code or debugging statements

## Dependencies

**User Story Order**: US1 → US2 → US3 (Each story builds on the foundational model work)

**Critical Path**: T004 → T005 → T008 → T009 → T010 (Model changes must happen before UI can be implemented)

## Parallel Execution Opportunities

**Within US1**: T007, T008, T009 can run in parallel with T010, T011
**Within US2**: T014, T015 can run in parallel
**Within US3**: T018 can be done independently after foundational work