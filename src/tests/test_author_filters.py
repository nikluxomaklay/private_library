"""
Tests for Author filter functionality.
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
from core.models import Author
from core.filters import AuthorFilter


class TestAuthorFilter(TestCase):
    """Test cases for Author filtering functionality."""

    def setUp(self):
        """Set up test data for Author filtering tests."""
        # Create test authors
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Doe",
            middle_name="Michael"
        )
        
        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Smith",
            middle_name="Elizabeth"
        )
        
        self.author3 = Author.objects.create(
            first_name="Bob",
            last_name="Johnson",
            middle_name="Robert"
        )

    def test_filter_by_full_name_substring(self):
        """Test filtering authors by full name substring."""
        # Test with first name
        filter_params = {'full_name': 'John'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)  # John Doe
        self.assertNotIn(self.author2, qs)  # Jane Smith
        self.assertNotIn(self.author3, qs)  # Bob Johnson
        
        # Test with last name
        filter_params = {'full_name': 'Smith'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.author1, qs)  # John Doe
        self.assertIn(self.author2, qs)  # Jane Smith
        self.assertNotIn(self.author3, qs)  # Bob Johnson
        
        # Test with middle name
        filter_params = {'full_name': 'Robert'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.author1, qs)  # John Doe
        self.assertNotIn(self.author2, qs)  # Jane Smith
        self.assertIn(self.author3, qs)  # Bob Johnson
        
        # Test with partial name
        filter_params = {'full_name': 'Ja'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.author1, qs)  # John Doe
        self.assertIn(self.author2, qs)  # Jane Smith
        self.assertNotIn(self.author3, qs)  # Bob Johnson

    def test_filter_case_insensitive(self):
        """Test that filtering is case insensitive."""
        # Test lowercase
        filter_params = {'full_name': 'john'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)  # John Doe
        
        # Test uppercase
        filter_params = {'full_name': 'JOHN'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)  # John Doe

    def test_filter_no_results(self):
        """Test filtering with non-existent name."""
        filter_params = {'full_name': 'Nonexistent'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)

    def test_filter_partial_matching(self):
        """Test that partial matching works correctly."""
        # Create an author with a longer name
        author_long = Author.objects.create(
            first_name="Alexander",
            last_name="McAllister-Smith",
            middle_name="Benjamin"
        )
        
        # Test partial match on first part of hyphenated last name
        filter_params = {'full_name': 'McAllister'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(author_long, qs)
        
        # Test partial match on second part of hyphenated last name
        filter_params = {'full_name': 'Smith'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(author_long, qs)

    def test_character_limit_validation(self):
        """Test that character limit validation works for text filters."""
        # Create a very long string (>255 chars)
        long_string = "A" * 300
        
        # Test filter with long string
        filter_params = {'full_name': long_string}
        filter_set = AuthorFilter(data=filter_params)
        
        # The filter should still work but may not match anything
        # The validation happens during form processing
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset

    def test_special_character_handling(self):
        """Test that special characters are handled properly."""
        # Create an author with special characters in name
        special_author = Author.objects.create(
            first_name="Mary",
            last_name="O'Connor",
            middle_name="Mc'Donald"
        )
        
        # Test filtering with apostrophe
        filter_params = {'full_name': "O'Connor"}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_author, qs)
        
        # Test filtering with another special character pattern
        filter_params = {'full_name': "Mc'Donald"}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_author, qs)