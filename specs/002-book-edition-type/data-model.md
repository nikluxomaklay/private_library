# Data Model for Book Edition Type Feature

## Updated BookEdition Model

### Fields
- `edition_type` (CharField with choices)
  - Choices: 'PAPER_BOOK', 'EBOOK', 'AUDIOBOOK', 'WEBPAGE'
  - Default: 'PAPER_BOOK'
  - Required: True
  - Max length: 20 characters
  - Help text: "Type of book edition"

### Relationships
- BookEdition remains connected to other existing models as before
- No new relationships introduced

### Validation Rules
- Field is required during creation
- Value must be one of the predefined choices
- Field becomes immutable after creation (enforced in form/view layer)

## Constants for Edition Types

### Type Values
- PAPER_BOOK: "Paper Book" (display), 📖 (icon)
- EBOOK: "E-book" (display), 📄 (icon)
- AUDIOBOOK: "Audiobook" (display), 🎙️ (icon)
- WEBPAGE: "Web Page" (display), 🌐 (icon)

### Business Logic
- Default type is 'PAPER_BOOK' when not explicitly selected
- Type cannot be modified after creation
- Icons are used for list view display
- Full text names are used for detail view display
- Use data-migration to fill type for existed book editions with default value