<!-- Sync Impact Report:
- Version change: N/A → 1.0.0
- Added sections: All principles and sections as defined below
- Templates requiring updates: 
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
- Follow-up TODOs: RATIFICATION_DATE
-->
# Private Library Constitution

## Core Principles

### I. Model-First
Every feature starts as a well-defined Django model; Models must be self-contained, independently testable, documented; Clear purpose required - no organizational-only models.

### II. Admin Interface
Every model exposes functionality via Django admin; Standard CRUD operations: create, read, update, delete via admin interface; Support for advanced filtering and search.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced.

### IV. Integration Testing
Focus areas requiring integration tests: New model relationships, Model changes, Inter-model communication, Shared schemas.

### V. Observability
Text I/O ensures debuggability; Structured logging required; MAJOR.MINOR.BUILD format for versioning; Start simple, YAGNI principles.

## Development Workflow

Code review requirements, testing gates, deployment approval process, etc.

## Additional Constraints

Technology stack requirements, compliance standards, deployment policies, etc.

## Governance

All PRs/reviews must verify compliance; Complexity must be justified; Use development guidelines for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-02-08