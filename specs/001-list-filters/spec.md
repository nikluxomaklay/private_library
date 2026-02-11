# Feature Specification: List Filters

**Feature Branch**: `001-list-filters`
**Created**: 11 февраля 2026
**Status**: Draft
**Input**: User description: "Добавить фильтрацию для страниц со списками (Reading log, Authors, Books, Book editions, Publishers, Book series)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Filter Reading Log Entries (Priority: P1)

As a user, I want to filter my reading log by various criteria including publication year, month, book title, author name, publisher, publication year, and book series to quickly find specific entries in my reading history.

**Why this priority**: This is the most important filter since the reading log is the central record of user activity and contains the most diverse data that users would want to search through.

**Independent Test**: Can be fully tested by applying different combinations of filters on the reading log page and verifying that only matching entries are displayed, delivering the value of quickly finding specific books in the reading history.

**Acceptance Scenarios**:

1. **Given** user is on the reading log page, **When** user applies year 'from' and 'to' filters, **Then** only entries with publication years within the specified range are shown
2. **Given** user is on the reading log page, **When** user enters a book title substring in the search field, **Then** only entries with titles containing that substring are shown
3. **Given** user is on the reading log page, **When** user enters an author name substring in the search field, **Then** only entries with authors whose names contain that substring are shown

---

### User Story 2 - Filter Authors List (Priority: P2)

As a user, I want to filter the authors list by name to quickly find specific authors in the database.

**Why this priority**: This is important for users who want to browse or find specific authors without scrolling through potentially long lists.

**Independent Test**: Can be fully tested by entering different substrings in the author name filter and verifying that only matching authors are displayed, delivering the value of quickly finding specific authors.

**Acceptance Scenarios**:

1. **Given** user is on the authors page, **When** user enters an author name substring in the search field, **Then** only authors whose names contain that substring are shown

---

### User Story 3 - Filter Books List (Priority: P2)

As a user, I want to filter the books list by title and author name to quickly find specific books in the database.

**Why this priority**: This is important for users who want to browse or find specific books without scrolling through potentially long lists.

**Independent Test**: Can be fully tested by entering different substrings in the book title and author name filters and verifying that only matching books are displayed, delivering the value of quickly finding specific books.

**Acceptance Scenarios**:

1. **Given** user is on the books page, **When** user enters a book title substring in the search field, **Then** only books whose titles contain that substring are shown
2. **Given** user is on the books page, **When** user enters an author name substring in the search field, **Then** only books by authors whose names contain that substring are shown

---

### User Story 4 - Filter Book Editions List (Priority: P3)

As a user, I want to filter the book editions list by title, author, publisher, publication year, and book series to find specific editions.

**Why this priority**: This is useful for users who want to find specific editions of books with particular characteristics.

**Independent Test**: Can be fully tested by applying different combinations of filters on the book editions page and verifying that only matching editions are displayed, delivering the value of quickly finding specific book editions.

**Acceptance Scenarios**:

1. **Given** user is on the book editions page, **When** user enters a book title substring in the search field, **Then** only editions with titles containing that substring are shown
2. **Given** user is on the book editions page, **When** user enters a publisher name substring in the search field, **Then** only editions from publishers whose names contain that substring are shown

---

### User Story 5 - Filter Publishers List (Priority: P3)

As a user, I want to filter the publishers list by name to quickly find specific publishers in the database.

**Why this priority**: This is useful for users who want to browse or find specific publishers without scrolling through potentially long lists.

**Independent Test**: Can be fully tested by entering different substrings in the publisher name filter and verifying that only matching publishers are displayed, delivering the value of quickly finding specific publishers.

**Acceptance Scenarios**:

1. **Given** user is on the publishers page, **When** user enters a publisher name substring in the search field, **Then** only publishers whose names contain that substring are shown

---

### User Story 6 - Filter Book Series List (Priority: P3)

As a user, I want to filter the book series list by name to quickly find specific book series in the database.

**Why this priority**: This is useful for users who want to browse or find specific book series without scrolling through potentially long lists.

**Independent Test**: Can be fully tested by entering different substrings in the book series name filter and verifying that only matching series are displayed, delivering the value of quickly finding specific book series.

**Acceptance Scenarios**:

1. **Given** user is on the book series page, **When** user enters a book series name substring in the search field, **Then** only series whose names contain that substring are shown

---

### Edge Cases

- What happens when a user enters special characters in the search fields?
- How does the system handle empty filter values?
- What happens when no results match the applied filters?
- How does the system handle very long search terms?
- What happens when the user clears all filters?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide year 'from' and/or 'to' selectors for filtering the Reading Log
- **FR-002**: System MUST provide month 'from' and/or 'to' selectors for filtering the Reading Log
- **FR-003**: System MUST provide combined year+month 'from' and/or 'to' selectors for filtering the Reading Log
- **FR-004**: System MUST provide book title search by substring for filtering the Reading Log
- **FR-005**: System MUST provide author name search by substring for filtering the Reading Log
- **FR-006**: System MUST provide publisher name search by substring for filtering the Reading Log
- **FR-007**: System MUST provide publication year exact match filter for the Reading Log
- **FR-008**: System MUST provide book series name search by substring for filtering the Reading Log
- **FR-009**: System MUST provide author name search by substring for filtering the Authors page
- **FR-010**: System MUST provide book title search by substring for filtering the Books page
- **FR-011**: System MUST provide author name search by substring for filtering the Books page
- **FR-012**: System MUST provide book title search by substring for filtering the Book Editions page
- **FR-013**: System MUST provide author name search by substring for filtering the Book Editions page
- **FR-014**: System MUST provide publisher name search by substring for filtering the Book Editions page
- **FR-015**: System MUST provide publication year exact match filter for the Book Editions page
- **FR-016**: System MUST provide book series name search by substring for filtering the Book Editions page
- **FR-017**: System MUST provide publisher name search by substring for filtering the Publishers page
- **FR-018**: System MUST provide book series name search by substring for filtering the Book Series page
- **FR-019**: System MUST maintain the same input styling as existing content addition pages for all filter inputs
- **FR-020**: System MUST allow clearing all applied filters with a single action
- **FR-021**: System MUST reset filters when navigating away from a filtered page and returning
- **FR-022**: System MUST display appropriate message when no results match the applied filters
- **FR-023**: System MUST sanitize special characters in search inputs to prevent injection attacks while preserving legitimate special characters in names
- **FR-024**: System MUST allow anonymous access to all filter functionality without requiring authentication
- **FR-025**: System MUST implement partial matching for all search fields designated as 'поиск по подстроке', finding entries that contain the search term anywhere in the field
- **FR-026**: System MUST limit search terms to 255 characters to prevent potential performance issues and match common database field limits
- **FR-027**: System MUST show an empty list/table with no specific indication when no results match the applied filters

### Key Entities *(include if feature involves data)*

- **Reading Log Entry**: Represents a record of a book that a user has read, with attributes like book title, author, publisher, publication year, and reading dates
- **Book**: Represents a literary work with attributes like title, author, and associated editions
- **Author**: Represents a person who wrote one or more books, with attributes like full name
- **Publisher**: Represents a company that published books, with attributes like name
- **Book Edition**: Represents a specific edition of a book with attributes like title, author, publisher, publication year, and book series
- **Book Series**: Represents a sequence of books with common themes or characters, with attributes like name

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can filter reading log entries by any combination of available criteria and see results updated within 2 seconds
- **SC-002**: Users can filter authors, books, book editions, publishers, and book series lists by name with results updated within 2 seconds
- **SC-003**: 95% of users can successfully apply filters and find desired entries without assistance
- **SC-004**: Filter input fields have the same visual appearance and behavior as existing input fields in the application
- **SC-005**: Users can clear all filters with a single action and return to the unfiltered view
- **SC-006**: When no results match the applied filters, users see a clear message indicating this situation

## Clarifications

### Session 2026-02-11

- Q: How should special characters in search fields be handled to prevent security issues? → A: Special characters in search fields should be sanitized/escaped to prevent injection attacks but still allow legitimate special characters in book/author names
- Q: Should filter functionality require user authentication? → A: Authentication not needed. Now all users of system is anonymous.
- Q: For fields specified as 'Поиск по подстроке', should partial matches be used? → A: For all fields specified as 'Поиск по подстроке' need to use partial matches.
- Q: What should be the character limit for search terms? → A: Limit search terms to 255 characters which is a common database field limit.
- Q: When no results match applied filters, what should be displayed? → A: Show an empty list/table with no indication of why it's empty.