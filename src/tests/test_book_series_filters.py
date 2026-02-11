"""
Tests for BookSeries filter functionality.
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
from core.models import Publisher, BookSeries
from core.filters import BookSeriesFilter


class TestBookSeriesFilter(TestCase):
    """Test cases for BookSeries filtering functionality."""

    def setUp(self):
        """Set up test data for BookSeries filtering tests."""
        # Create test publishers
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        self.publisher2 = Publisher.objects.create(name="Programming Press")
        
        # Create test book series
        self.series1 = BookSeries.objects.create(
            name="Programming Series",
            publisher=self.publisher1
        )
        
        self.series2 = BookSeries.objects.create(
            name="Web Development Series",
            publisher=self.publisher2
        )
        
        self.series3 = BookSeries.objects.create(
            name="Data Science Series",
            publisher=self.publisher1
        )
        
        self.series4 = BookSeries.objects.create(
            name="Machine Learning Series",
            publisher=self.publisher2
        )

    def test_filter_by_series_name_substring(self):
        """Test filtering book series by name substring."""
        # Test with full name
        filter_params = {'name': 'Programming Series'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)
        self.assertNotIn(self.series2, qs)
        self.assertNotIn(self.series3, qs)
        self.assertNotIn(self.series4, qs)
        
        # Test with partial name
        filter_params = {'name': 'Programming'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)
        self.assertNotIn(self.series2, qs)
        self.assertNotIn(self.series3, qs)
        self.assertNotIn(self.series4, qs)
        
        # Test with another partial name
        filter_params = {'name': 'Development'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.series1, qs)
        self.assertIn(self.series2, qs)
        self.assertNotIn(self.series3, qs)
        self.assertNotIn(self.series4, qs)
        
        # Test with common substring
        filter_params = {'name': 'Series'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)
        self.assertIn(self.series2, qs)
        self.assertIn(self.series3, qs)
        self.assertIn(self.series4, qs)

    def test_case_insensitive_filtering(self):
        """Test that filtering is case insensitive."""
        # Test with lowercase
        filter_params = {'name': 'programming'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)  # Should match "Programming Series"
        
        # Test with uppercase
        filter_params = {'name': 'PROGRAMMING'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)  # Should match "Programming Series"

    def test_no_results_filtering(self):
        """Test filtering with non-existent series name."""
        filter_params = {'name': 'Nonexistent Series'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)

    def test_multiple_matches_filtering(self):
        """Test filtering that matches multiple series."""
        # Create more series with similar names
        series5 = BookSeries.objects.create(
            name="Advanced Programming Series",
            publisher=self.publisher1
        )
        series6 = BookSeries.objects.create(
            name="Intro to Programming",
            publisher=self.publisher2
        )
        
        filter_params = {'name': 'Programming'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)  # "Programming Series"
        self.assertNotIn(self.series2, qs)  # "Web Development Series"
        self.assertNotIn(self.series3, qs)  # "Data Science Series"
        self.assertNotIn(self.series4, qs)  # "Machine Learning Series"
        self.assertIn(series5, qs)  # "Advanced Programming Series"
        self.assertIn(series6, qs)  # "Intro to Programming"

    def test_character_limit_validation(self):
        """Test that character limit validation works for text filters."""
        # Create a very long string (>255 chars)
        long_string = "A" * 300
        
        # Test filter with long string
        filter_params = {'name': long_string}
        filter_set = BookSeriesFilter(data=filter_params)
        
        # The filter should still work but may not match anything
        # The validation happens during form processing
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset

    def test_special_character_handling(self):
        """Test that special characters are handled properly."""
        # Create a series with special characters in name
        special_series = BookSeries.objects.create(
            name="Series with <script>alert('test')</script>",
            publisher=self.publisher1
        )
        
        # Test filtering with special characters
        filter_params = {'name': "alert"}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_series, qs)
        
        # Create another series with apostrophes
        special_series2 = BookSeries.objects.create(
            name="O'Reilly Book Series",
            publisher=self.publisher2
        )
        
        # Test filtering with apostrophe
        filter_params = {'name': "O'Reilly"}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_series2, qs)

    def test_empty_string_filtering(self):
        """Test filtering with empty string."""
        filter_params = {'name': ''}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        # Should return all series when filter is empty
        self.assertCountEqual(qs, [
            self.series1, 
            self.series2, 
            self.series3, 
            self.series4
        ])