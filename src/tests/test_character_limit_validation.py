"""
Tests for character limit validation on text-based filters.
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


class TestCharacterLimitValidation(TestCase):
    """Test cases for character limit validation (255 chars) on text-based filters."""

    def setUp(self):
        """Set up test data for character limit validation tests."""
        # Create test data
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Doe"
        )
        
        self.book1 = Book.objects.create(
            title="Test Book"
        )
        self.book1.authors.add(self.author1)
        
        self.publisher1 = Publisher.objects.create(
            name="Test Publisher"
        )
        
        self.series1 = BookSeries.objects.create(
            name="Test Series",
            publisher=self.publisher1
        )
        
        self.year_2020 = Year.objects.create(year=2020)
        
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

    def test_reading_log_filter_character_limits(self):
        """Test ReadingLog filter character limits."""
        # Test with 255 characters (should work)
        long_string_255 = "A" * 255
        filter_params = {'book_title': long_string_255}
        filter_set = ReadingLogFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        # Test with 256 characters (might not match anything but shouldn't crash)
        long_string_256 = "A" * 256
        filter_params = {'book_title': long_string_256}
        filter_set = ReadingLogFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_author_filter_character_limits(self):
        """Test Author filter character limits."""
        long_string_255 = "A" * 255
        filter_params = {'full_name': long_string_255}
        filter_set = AuthorFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        long_string_256 = "A" * 256
        filter_params = {'full_name': long_string_256}
        filter_set = AuthorFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_book_filter_character_limits(self):
        """Test Book filter character limits."""
        long_string_255 = "A" * 255
        filter_params = {'title': long_string_255}
        filter_set = BookFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        filter_params = {'author_name': long_string_255}
        filter_set = BookFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        long_string_256 = "A" * 256
        filter_params = {'title': long_string_256}
        filter_set = BookFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_book_edition_filter_character_limits(self):
        """Test BookEdition filter character limits."""
        long_string_255 = "A" * 255
        filter_params = {'book_title': long_string_255}
        filter_set = BookEditionFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        filter_params = {'author_name': long_string_255}
        filter_set = BookEditionFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        filter_params = {'publisher_name': long_string_255}
        filter_set = BookEditionFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        filter_params = {'book_series_name': long_string_255}
        filter_set = BookEditionFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        long_string_256 = "A" * 256
        filter_params = {'book_title': long_string_256}
        filter_set = BookEditionFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_publisher_filter_character_limits(self):
        """Test Publisher filter character limits."""
        long_string_255 = "A" * 255
        filter_params = {'name': long_string_255}
        filter_set = PublisherFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        long_string_256 = "A" * 256
        filter_params = {'name': long_string_256}
        filter_set = PublisherFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_book_series_filter_character_limits(self):
        """Test BookSeries filter character limits."""
        long_string_255 = "A" * 255
        filter_params = {'name': long_string_255}
        filter_set = BookSeriesFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset
        
        long_string_256 = "A" * 256
        filter_params = {'name': long_string_256}
        filter_set = BookSeriesFilter(data=filter_params)
        # This should not raise an exception
        qs = filter_set.qs
        list(qs)  # Evaluate the queryset

    def test_character_limit_validation_method(self):
        """Test the character limit validation method directly."""
        from core.filters import BaseFilterSet
        base_filter = BaseFilterSet()
        
        # Test valid length (under 255)
        valid_string = "A" * 200
        result = base_filter.validate_char_limit(valid_string)
        self.assertEqual(result, valid_string)
        
        # Test exact 255 characters
        exact_limit_string = "A" * 255
        result = base_filter.validate_char_limit(exact_limit_string)
        self.assertEqual(result, exact_limit_string)
        
        # Test over 255 characters - should raise ValidationError
        from django.core.exceptions import ValidationError
        over_limit_string = "A" * 256
        with self.assertRaises(ValidationError):
            base_filter.validate_char_limit(over_limit_string)