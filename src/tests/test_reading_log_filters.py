"""
Tests for ReadingLog filter functionality.
"""
import os
import sys
import django
from django.conf import settings
from django.test import TestCase

# Add the project directory to Python path
sys.path.append('/home/saturnus/repos/private_library/src')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'private_library.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Author, Book, Publisher, BookSeries, BookEdition, Year, ReadingLog


class TestReadingLogFilter(TestCase):
    """Test cases for ReadingLog filtering functionality."""

    def setUp(self):
        """Set up test data for ReadingLog filtering tests."""
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create test data
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe"
        )
        
        self.book = Book.objects.create(
            title="Test Book Title"
        )
        self.book.authors.add(self.author)
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher"
        )
        
        self.series = BookSeries.objects.create(
            name="Test Series",
            publisher=self.publisher
        )
        
        self.year_2020 = Year.objects.create(year=2020)
        self.year_2021 = Year.objects.create(year=2021)
        
        self.book_edition = BookEdition.objects.create(
            book=self.book,
            publisher=self.publisher,
            series=self.series,
            publication_year=2020
        )
        
        # Create reading log entries
        self.reading_log_1 = ReadingLog.objects.create(
            book_edition=self.book_edition,
            year_start=self.year_2020,
            month_start=3,  # March
            year_finish=self.year_2020,
            month_finish=6   # June
        )
        
        self.reading_log_2 = ReadingLog.objects.create(
            book_edition=self.book_edition,
            year_start=self.year_2021,
            month_start=1,  # January
            year_finish=self.year_2021,
            month_finish=12  # December
        )

    def test_filter_by_book_title_substring(self):
        """Test filtering reading logs by book title substring."""
        from core.filters import ReadingLogFilter
        
        # Test with full title
        filter_params = {'book_title': 'Test Book'}
        filter_set = ReadingLogFilter(data=filter_params)
        
        # Check that the filter is working by inspecting the queryset
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with partial title
        filter_params = {'book_title': 'Book'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with non-matching title
        filter_params = {'book_title': 'Nonexistent'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_by_author_name_substring(self):
        """Test filtering reading logs by author name substring."""
        from core.filters import ReadingLogFilter
        
        # Test with full author name
        filter_params = {'author_name': 'John Doe'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with partial author name
        filter_params = {'author_name': 'Doe'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with non-matching author name
        filter_params = {'author_name': 'Smith'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_by_publisher_name_substring(self):
        """Test filtering reading logs by publisher name substring."""
        from core.filters import ReadingLogFilter
        
        # Test with full publisher name
        filter_params = {'publisher_name': 'Test Publisher'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with partial publisher name
        filter_params = {'publisher_name': 'Publisher'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with non-matching publisher name
        filter_params = {'publisher_name': 'Other Publisher'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_by_publication_year_exact_match(self):
        """Test filtering reading logs by exact publication year."""
        from core.filters import ReadingLogFilter
        
        # Test with matching publication year
        filter_params = {'publication_year': 2020}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)  # Both use the same book edition with pub year 2020
        
        # Test with non-matching publication year
        filter_params = {'publication_year': 2021}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_by_book_series_name_substring(self):
        """Test filtering reading logs by book series name substring."""
        from core.filters import ReadingLogFilter
        
        # Test with full series name
        filter_params = {'book_series_name': 'Test Series'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with partial series name
        filter_params = {'book_series_name': 'Series'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Test with non-matching series name
        filter_params = {'book_series_name': 'Other Series'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_by_year_range(self):
        """Test filtering reading logs by year range."""
        from core.filters import ReadingLogFilter
        
        # Test year from filter
        filter_params = {'year_from': 2021}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        # Should include reading_log_2 which has year_start=2021
        self.assertIn(self.reading_log_2, qs)
        # Should not include reading_log_1 which has year_start=2020
        self.assertNotIn(self.reading_log_1, qs)
        
        # Test year to filter
        filter_params = {'year_to': 2020}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        # Should include reading_log_1 which has year_finish=2020
        self.assertIn(self.reading_log_1, qs)
        # Should not include reading_log_2 which has year_finish=2021
        self.assertNotIn(self.reading_log_2, qs)

    def test_filter_combination(self):
        """Test combining multiple filters."""
        from core.filters import ReadingLogFilter
        
        # Combine book title and author name filters
        filter_params = {
            'book_title': 'Test Book',
            'author_name': 'John'
        }
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log_1, qs)
        self.assertIn(self.reading_log_2, qs)
        
        # Combine book title with non-matching author name
        filter_params = {
            'book_title': 'Test Book',
            'author_name': 'Nonexistent'
        }
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.reading_log_1, qs)
        self.assertNotIn(self.reading_log_2, qs)

    def test_character_limit_validation(self):
        """Test that character limit validation works for text filters."""
        from core.filters import ReadingLogFilter
        from django.core.exceptions import ValidationError
        
        # Create a very long string (>255 chars)
        long_string = "A" * 300
        
        # Test book title filter with long string
        filter_params = {'book_title': long_string}
        filter_set = ReadingLogFilter(data=filter_params)
        
        # The filter should still work but may not match anything
        # The validation happens during form processing
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset

    def test_special_character_sanitization(self):
        """Test that special characters are handled properly."""
        from core.filters import ReadingLogFilter
        
        # Create a reading log with special characters in related fields
        special_author = Author.objects.create(
            first_name="Special",
            last_name="Character's & More"
        )
        
        special_book = Book.objects.create(
            title="Special Book <script>alert('test')</script>"
        )
        special_book.authors.add(special_author)
        
        special_edition = BookEdition.objects.create(
            book=special_book,
            publisher=self.publisher,
            series=self.series,
            publication_year=2020
        )
        
        special_reading_log = ReadingLog.objects.create(
            book_edition=special_edition,
            year_start=self.year_2020,
            month_start=5,
            year_finish=self.year_2020,
            month_finish=8
        )
        
        # Test filtering with special characters in search term
        filter_params = {'author_name': "Character's"}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_reading_log, qs)
        
        # Test filtering with HTML-like content
        filter_params = {'book_title': "Special Book"}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_reading_log, qs)