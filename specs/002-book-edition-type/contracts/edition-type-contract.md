# API Contract for Book Edition Type

## Overview
This contract defines the expected behavior for the book edition type functionality in the private library system.

## Data Model Contract

### BookEdition Object Extension
```
{
  "id": integer,
  "title": string,
  "author": string,
  // ... existing fields
  "edition_type": {
    "type": "string",
    "enum": ["PAPER_BOOK", "EBOOK", "AUDIOBOOK", "WEBPAGE"],
    "default": "PAPER_BOOK",
    "required": true,
    "immutable_after_creation": true
  }
}
```

## UI Contract

### Creation Form
- Field: `edition_type`
- Type: Dropdown/Select
- Options: Paper Book, E-book, Audiobook, Web Page
- Default: Paper Book
- Validation: Required field
- Behavior: Form should not submit without selection

### List View
- Display: Unicode icon corresponding to edition type
- Icons: 📖 (Paper Book), 📄 (E-book), 🎙️ (Audiobook), 🌐 (Web Page)
- Position: At the end of each row, after a dash separator

### Detail View
- Display: Full text name of the edition type
- Label: "Edition Type" followed by the type name
- Position: Alongside other book properties

## Backend Contract

### Validation Rules
- On creation: edition_type must be one of the allowed values
- On creation: if no value provided, default to "PAPER_BOOK"
- On update: edition_type field should be ignored or raise validation error
- On storage: value must match one of the enum values

### Default Behavior
- When creating a new BookEdition without specifying edition_type, the system should assign "PAPER_BOOK"
- The edition_type field should be required in all contexts