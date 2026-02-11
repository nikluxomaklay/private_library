"""
Tests for special character handling and sanitization in filters.
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
from core.filters import ReadingLogFilter, AuthorFilter, BookFilter, BookEditionFilter, PublisherFilter, BookSeriesFilter


class TestSpecialCharacterHandling(TestCase):
    """Test cases for special character handling and sanitization in filters."""

    def setUp(self):
        """Set up test data for special character handling tests."""
        # Create test data with special characters
        self.author1 = Author.objects.create(
            first_name="Mary",
            last_name="O'Connor"
        )
        
        self.author2 = Author.objects.create(
            first_name="John",
            last_name="Smith-Jones"
        )
        
        self.book1 = Book.objects.create(
            title="Book with <script>alert('test')</script> code"
        )
        self.book1.authors.add(self.author1)
        
        self.book2 = Book.objects.create(
            title="Another book & special chars"
        )
        self.book2.authors.add(self.author2)
        
        self.publisher1 = Publisher.objects.create(
            name="Publisher with 'quotes' and \"double quotes\""
        )
        
        self.series1 = BookSeries.objects.create(
            name="Series with <html> tags",
            publisher=self.publisher1
        )
        
        self.year_2020 = Year.objects.create(year=2020)
        self.year_2021 = Year.objects.create(year=2021)
        
        self.book_edition1 = BookEdition.objects.create(
            book=self.book1,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2020
        )
        
        self.reading_log1 = ReadingLog.objects.create(
            book_edition=self.book_edition1,
            year_start=self.year_2020,
            month_start=3,
            year_finish=self.year_2020,
            month_finish=6
        )

    def test_reading_log_filter_special_characters(self):
        """Test ReadingLog filter with special characters."""
        filter_params = {'book_title': "alert"}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)
        
        # Test with quotes
        filter_params = {'author_name': "O'Connor"}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)

    def test_author_filter_special_characters(self):
        """Test Author filter with special characters."""
        filter_params = {'full_name': "O'Connor"}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)
        
        # Test with hyphens
        filter_params = {'full_name': "Smith-Jones"}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author2, qs)

    def test_book_filter_special_characters(self):
        """Test Book filter with special characters."""
        filter_params = {'title': "alert"}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book1, qs)
        
        # Test with ampersand
        filter_params = {'title': "special chars"}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book2, qs)
        
        # Test with special characters in author name
        filter_params = {'author_name': "O'Connor"}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book1, qs)

    def test_book_edition_filter_special_characters(self):
        """Test BookEdition filter with special characters."""
        filter_params = {'book_title': "alert"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book_edition1, qs)
        
        # Test with quotes in publisher name
        filter_params = {'publisher_name': "quotes"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book_edition1, qs)
        
        # Test with HTML tags in series name
        filter_params = {'book_series_name': "html"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book_edition1, qs)

    def test_publisher_filter_special_characters(self):
        """Test Publisher filter with special characters."""
        filter_params = {'name': "quotes"}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)

    def test_book_series_filter_special_characters(self):
        """Test BookSeries filter with special characters."""
        filter_params = {'name': "html"}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)

    def test_xss_prevention(self):
        """Test that XSS attempts are properly handled."""
        # Test with potential XSS in book title
        dangerous_book = Book.objects.create(
            title="<script>alert('xss')</script>Dangerous Book"
        )
        dangerous_book.authors.add(self.author1)
        
        dangerous_edition = BookEdition.objects.create(
            book=dangerous_book,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2021
        )
        
        # The filter should work without executing the script
        filter_params = {'book_title': "xss"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(dangerous_edition, qs)

    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are properly handled."""
        # django-filter uses Django's ORM which inherently protects against SQL injection
        # But we can test with special SQL characters
        sql_book = Book.objects.create(
            title="Book with ' quote and ; semicolon"
        )
        sql_book.authors.add(self.author1)
        
        sql_edition = BookEdition.objects.create(
            book=sql_book,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2021
        )
        
        # Test filtering with quote character
        filter_params = {'book_title': "'"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(sql_edition, qs)
        
        # Test filtering with semicolon character
        filter_params = {'book_title': ";"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(sql_edition, qs)

    def test_character_sanitization_in_base_filter(self):
        """Test that the base filter's sanitization works properly."""
        # Test the sanitize_special_chars method directly
        from core.filters import BaseFilterSet
        base_filter = BaseFilterSet()
        
        # Test HTML tag sanitization
        original = "<script>alert('test')</script>"
        sanitized = base_filter.sanitize_special_chars(original)
        expected = "&lt;script&gt;alert('test')&lt;/script&gt;"
        self.assertEqual(sanitized, expected)
        
        # Test that sanitized content still works in filters
        filter_params = {'book_title': "&lt;script&gt;"}
        filter_set = BookEditionFilter(data=filter_params)
        # This shouldn't cause any errors
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset to make sure it works