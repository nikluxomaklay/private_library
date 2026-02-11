# Implementation Plan: Book Edition Type

**Branch**: `002-book-edition-type` | **Date**: 11 февраля 2026 | **Spec**: [spec link](spec.md)
**Input**: Feature specification from `/specs/002-book-edition-type/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements the book edition type feature by adding a choice field to the existing BookEdition model. The solution includes a dropdown selection during creation with four predefined types (Paper Book, E-book, Audiobook, Web Page), defaulting to Paper Book. The implementation follows the Model-First principle, and displays icons in list views and text in detail views as required. The field is immutable after creation as specified in the feature requirements.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11
**Primary Dependencies**: Django 4.x, django-bootstrap5, django-autocomplete-light
**Storage**: PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Web application
**Performance Goals**: Standard web application performance (pages load under 2 seconds)
**Constraints**: Must integrate with existing interface, follow existing code patterns
**Scale/Scope**: Private library application with moderate number of users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Model-First Compliance
✓ New BookEditionType model will be created with clear purpose
✓ Model will be self-contained and independently testable
✓ Purpose is clearly defined (categorizing book editions by format)

### Test-First Compliance
✓ Tests will be written before implementation
✓ Following Red-Green-Refactor cycle
✓ TDD approach will be strictly enforced

### Integration Testing Compliance
✓ Will test relationships between BookEdition and BookEditionType
✓ Will test model changes and inter-model communication

### Observability Compliance
✓ Structured logging will be implemented where needed
✓ Following versioning standards
✓ Debuggability ensured through proper I/O

### Additional Constraints Compliance
✓ Using Django framework as required
✓ Using Django templates + django-bootstrap5 for frontend
✓ Using django-autocomplete-light for selectors
✓ Writing documentation in Russian
✓ Using named arguments in functions

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
private_library/
├── manage.py
└── src/
    ├── core/
    │   ├── models.py          # Contains BookEdition and BookEditionType models
    │   ├── views.py
    │   ├── forms.py
    │   ├── migrations/        # Database migrations
    │   └── ...
    ├── templates/
    │   ├── book_edition/
    │   │   ├── book_edition_list.html     # List view with icons
    │   │   ├── book_edition_update.html   # Detail view showing type
    │   │   ├── book_edition_new.html     # Creation form with dropdown
    │   │   └── ...
    │   └── ...
    ├── static/
    │   └── ...
    └── tests/
        ├── unit/
        │   └── test_models.py     # Unit tests for models
        ├── integration/
        │   └── test_views.py      # Integration tests for views
        └── ...

```

**Structure Decision**: Web application using Django project structure. The BookEditionType feature will be implemented in the existing books app, with model changes, and template modifications to support the new functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
