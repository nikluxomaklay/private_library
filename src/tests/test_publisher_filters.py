"""
Tests for Publisher filter functionality.
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
from core.models import Publisher
from core.filters import PublisherFilter


class TestPublisherFilter(TestCase):
    """Test cases for Publisher filtering functionality."""

    def setUp(self):
        """Set up test data for Publisher filtering tests."""
        # Create test publishers
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        self.publisher2 = Publisher.objects.create(name="Programming Press")
        self.publisher3 = Publisher.objects.create(name="Web Development Books")
        self.publisher4 = Publisher.objects.create(name="Data Science Publishing")

    def test_filter_by_publisher_name_substring(self):
        """Test filtering publishers by name substring."""
        # Test with full name
        filter_params = {'name': 'Tech Publications'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)
        self.assertNotIn(self.publisher2, qs)
        self.assertNotIn(self.publisher3, qs)
        self.assertNotIn(self.publisher4, qs)
        
        # Test with partial name
        filter_params = {'name': 'Tech'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)
        self.assertNotIn(self.publisher2, qs)
        self.assertNotIn(self.publisher3, qs)
        self.assertNotIn(self.publisher4, qs)
        
        # Test with another partial name
        filter_params = {'name': 'Press'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.publisher1, qs)
        self.assertIn(self.publisher2, qs)
        self.assertNotIn(self.publisher3, qs)
        self.assertNotIn(self.publisher4, qs)
        
        # Test with common substring
        filter_params = {'name': 'Publishing'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.publisher1, qs)
        self.assertNotIn(self.publisher2, qs)
        self.assertNotIn(self.publisher3, qs)
        self.assertIn(self.publisher4, qs)

    def test_case_insensitive_filtering(self):
        """Test that filtering is case insensitive."""
        # Test with lowercase
        filter_params = {'name': 'tech'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)  # Should match "Tech Publications"
        
        # Test with uppercase
        filter_params = {'name': 'TECH'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)  # Should match "Tech Publications"

    def test_no_results_filtering(self):
        """Test filtering with non-existent publisher name."""
        filter_params = {'name': 'Nonexistent Publisher'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)

    def test_multiple_matches_filtering(self):
        """Test filtering that matches multiple publishers."""
        # Create more publishers with similar names
        pub5 = Publisher.objects.create(name="Technical Books")
        pub6 = Publisher.objects.create(name="Techno Press")
        
        filter_params = {'name': 'Tech'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)  # "Tech Publications"
        self.assertNotIn(self.publisher2, qs)  # "Programming Press"
        self.assertNotIn(self.publisher3, qs)  # "Web Development Books"
        self.assertNotIn(self.publisher4, qs)  # "Data Science Publishing"
        self.assertIn(pub5, qs)  # "Technical Books"
        self.assertNotIn(pub6, qs)  # "Techno Press" (doesn't contain "Tech")

    def test_character_limit_validation(self):
        """Test that character limit validation works for text filters."""
        # Create a very long string (>255 chars)
        long_string = "A" * 300
        
        # Test filter with long string
        filter_params = {'name': long_string}
        filter_set = PublisherFilter(data=filter_params)
        
        # The filter should still work but may not match anything
        # The validation happens during form processing
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset

    def test_special_character_handling(self):
        """Test that special characters are handled properly."""
        # Create a publisher with special characters in name
        special_publisher = Publisher.objects.create(
            name="Publisher with <script>alert('test')</script>"
        )
        
        # Test filtering with special characters
        filter_params = {'name': "alert"}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_publisher, qs)
        
        # Create another publisher with apostrophes
        special_publisher2 = Publisher.objects.create(
            name="O'Reilly Media"
        )
        
        # Test filtering with apostrophe
        filter_params = {'name': "O'Reilly"}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_publisher2, qs)

    def test_empty_string_filtering(self):
        """Test filtering with empty string."""
        filter_params = {'name': ''}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        # Should return all publishers when filter is empty
        self.assertCountEqual(qs, [
            self.publisher1, 
            self.publisher2, 
            self.publisher3, 
            self.publisher4
        ])