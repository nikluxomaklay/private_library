# Data Model: List Filters

## Entities and Fields

### ReadingLog
- **Fields used for filtering**:
  - `book_title` (CharField) - for substring search
  - `author_name` (CharField) - for substring search  
  - `publisher_name` (CharField) - for substring search
  - `publication_year` (IntegerField) - for exact match and range filtering
  - `reading_date` (DateField) - for year/month range filtering
  - `book_series_name` (CharField) - for substring search

### Author
- **Fields used for filtering**:
  - `full_name` (CharField) - for substring search

### Book
- **Fields used for filtering**:
  - `title` (CharField) - for substring search
  - `authors` (ManyToManyField to Author) - for substring search on author names

### BookEdition
- **Fields used for filtering**:
  - `book_title` (CharField) - for substring search
  - `authors` (ManyToManyField to Author) - for substring search on author names
  - `publisher_name` (CharField) - for substring search
  - `publication_year` (IntegerField) - for exact match filtering
  - `book_series_name` (CharField) - for substring search

### Publisher
- **Fields used for filtering**:
  - `name` (CharField) - for substring search

### BookSeries
- **Fields used for filtering**:
  - `name` (CharField) - for substring search

## Validation Rules from Requirements

### FR-023: Sanitization of Special Characters
- All text search inputs must sanitize special characters to prevent injection attacks
- Implementation: Use django-filter which leverages Django's built-in ORM that handles SQL injection prevention
- For text searches, use `icontains` lookup which safely handles special characters

### FR-025: Partial Matching
- All 'поиск по подстроке' fields must implement partial matching
- Implementation: Use django-filter's CharFilter with lookup_expr='icontains' for substring matching

### FR-026: Character Limit
- All search terms must be limited to 255 characters
- Implementation: Add validation to django-filter forms to enforce 255 character limit

## Relationships Relevant to Filtering

### Book to Author
- Many-to-Many relationship allows filtering books by author name substring
- Through intermediate model if needed for additional metadata

### BookEdition to Book
- Foreign key relationship allows filtering editions by book title

### BookEdition to Author
- Many-to-Many relationship allows filtering editions by author name substring

## State Transitions (if applicable)
- N/A for this feature - filtering is a read operation that doesn't change entity states

## Indexing Strategy
- Add database indexes on fields commonly used for filtering:
  - `publication_year` on ReadingLog and BookEdition
  - `title` on Book and BookEdition
  - `name` on Author, Publisher, and BookSeries
  - `reading_date` on ReadingLog

## FilterSet Classes

### ReadingLogFilter
- Uses django-filter's FilterSet
- Includes filters for year ranges, month ranges, and text searches
- Implements custom filters for combined year+month functionality

### AuthorFilter
- Simple CharFilter for name substring search

### BookFilter
- CharFilter for title substring search
- Custom filter for author name search with django-autocomplete-light integration

### BookEditionFilter
- Multiple CharFilters for title, publisher, and series name
- NumberFilter for exact publication year matching
- Custom filter for author name search with django-autocomplete-light integration

### PublisherFilter
- Simple CharFilter for name substring search

### BookSeriesFilter
- Simple CharFilter for name substring search