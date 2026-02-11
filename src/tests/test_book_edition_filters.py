"""
Tests for BookEdition filter functionality.
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
from core.models import Author, Book, Publisher, BookSeries, BookEdition
from core.filters import BookEditionFilter


class TestBookEditionFilter(TestCase):
    """Test cases for BookEdition filtering functionality."""

    def setUp(self):
        """Set up test data for BookEdition filtering tests."""
        # Create test authors
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Doe"
        )
        
        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Smith"
        )
        
        # Create test books
        self.book1 = Book.objects.create(title="Django for Beginners")
        self.book1.authors.add(self.author1)
        
        self.book2 = Book.objects.create(title="Python Tricks")
        self.book2.authors.add(self.author2)
        
        # Create test publisher
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        self.publisher2 = Publisher.objects.create(name="Programming Press")
        
        # Create test series
        self.series1 = BookSeries.objects.create(
            name="Programming Series",
            publisher=self.publisher1
        )
        self.series2 = BookSeries.objects.create(
            name="Web Development Series",
            publisher=self.publisher2
        )
        
        # Create test book editions
        self.edition1 = BookEdition.objects.create(
            book=self.book1,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2022
        )
        
        self.edition2 = BookEdition.objects.create(
            book=self.book2,
            publisher=self.publisher2,
            series=self.series2,
            publication_year=2021
        )
        
        self.edition3 = BookEdition.objects.create(
            book=self.book1,  # Same book as edition1 but different edition
            publisher=self.publisher2,
            series=self.series1,
            publication_year=2023
        )

    def test_filter_by_book_title_substring(self):
        """Test filtering book editions by book title substring."""
        # Test with full title
        filter_params = {'book_title': 'Django for Beginners'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)
        self.assertNotIn(self.edition2, qs)
        self.assertIn(self.edition3, qs)  # Also has the same book
        
        # Test with partial title
        filter_params = {'book_title': 'Django'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)
        self.assertNotIn(self.edition2, qs)
        self.assertIn(self.edition3, qs)  # Also has the same book
        
        # Test with another partial title
        filter_params = {'book_title': 'Python'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)
        self.assertIn(self.edition2, qs)
        self.assertNotIn(self.edition3, qs)

    def test_filter_by_author_name_substring(self):
        """Test filtering book editions by author name substring."""
        # Test with author name that appears in multiple editions
        filter_params = {'author_name': 'John'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Has John Doe as author
        self.assertNotIn(self.edition2, qs)  # Has Jane Smith as author
        self.assertIn(self.edition3, qs)  # Also has John Doe as author (same book)
        
        # Test with another author name
        filter_params = {'author_name': 'Smith'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)  # Has John Doe as author
        self.assertIn(self.edition2, qs)  # Has Jane Smith as author
        self.assertNotIn(self.edition3, qs)  # Has John Doe as author

    def test_filter_by_publisher_name_substring(self):
        """Test filtering book editions by publisher name substring."""
        # Test with partial publisher name
        filter_params = {'publisher_name': 'Tech'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Published by Tech Publications
        self.assertNotIn(self.edition2, qs)  # Published by Programming Press
        self.assertNotIn(self.edition3, qs)  # Published by Programming Press
        
        # Test with another partial publisher name
        filter_params = {'publisher_name': 'Press'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)  # Published by Tech Publications
        self.assertIn(self.edition2, qs)  # Published by Programming Press
        self.assertIn(self.edition3, qs)  # Published by Programming Press

    def test_filter_by_publication_year_exact_match(self):
        """Test filtering book editions by exact publication year."""
        # Test with specific year
        filter_params = {'publication_year': 2022}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Published in 2022
        self.assertNotIn(self.edition2, qs)  # Published in 2021
        self.assertNotIn(self.edition3, qs)  # Published in 2023
        
        # Test with another year
        filter_params = {'publication_year': 2021}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)  # Published in 2022
        self.assertIn(self.edition2, qs)  # Published in 2021
        self.assertNotIn(self.edition3, qs)  # Published in 2023

    def test_filter_by_book_series_name_substring(self):
        """Test filtering book editions by book series name substring."""
        # Test with partial series name
        filter_params = {'book_series_name': 'Programming'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Part of Programming Series
        self.assertNotIn(self.edition2, qs)  # Part of Web Development Series
        self.assertIn(self.edition3, qs)  # Part of Programming Series
        
        # Test with another partial series name
        filter_params = {'book_series_name': 'Development'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)  # Part of Programming Series
        self.assertIn(self.edition2, qs)  # Part of Web Development Series
        self.assertNotIn(self.edition3, qs)  # Part of Programming Series

    def test_combined_filtering(self):
        """Test combining multiple filters."""
        # Find editions published by 'Tech' in year 2022
        filter_params = {
            'publisher_name': 'Tech',
            'publication_year': 2022
        }
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Matches both criteria
        self.assertNotIn(self.edition2, qs)  # Doesn't match publisher
        self.assertNotIn(self.edition3, qs)  # Doesn't match either criterion
        
        # Find editions with 'Django' in title published by 'Programming'
        filter_params = {
            'book_title': 'Django',
            'publisher_name': 'Programming'
        }
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.edition1, qs)  # Matches title but not publisher
        self.assertNotIn(self.edition2, qs)  # Matches publisher but not title
        self.assertIn(self.edition3, qs)  # Same book as edition1 (Django) but published by Programming

    def test_case_insensitive_filtering(self):
        """Test that filtering is case insensitive."""
        # Test book title filter with different case
        filter_params = {'book_title': 'django'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # 'Django for Beginners' should match 'django'
        self.assertIn(self.edition3, qs)  # Same book as edition1
        
        # Test author filter with different case
        filter_params = {'author_name': 'doe'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Should match John Doe
        self.assertIn(self.edition3, qs)  # Should match John Doe (same book)
        
        # Test publisher filter with different case
        filter_params = {'publisher_name': 'tech'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.edition1, qs)  # Should match Tech Publications

    def test_no_results_filtering(self):
        """Test filtering with non-existent values."""
        filter_params = {'book_title': 'Nonexistent Book'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)
        
        filter_params = {'author_name': 'Nonexistent Author'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)
        
        filter_params = {'publisher_name': 'Nonexistent Publisher'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertEqual(qs.count(), 0)

    def test_character_limit_validation(self):
        """Test that character limit validation works for text filters."""
        # Create a very long string (>255 chars)
        long_string = "A" * 300
        
        # Test book title filter with long string
        filter_params = {'book_title': long_string}
        filter_set = BookEditionFilter(data=filter_params)
        
        # The filter should still work but may not match anything
        # The validation happens during form processing
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset
        
        # Test author name filter with long string
        filter_params = {'author_name': long_string}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        # This should not raise an exception
        list(qs)  # Force evaluation of the queryset

    def test_special_character_handling(self):
        """Test that special characters are handled properly."""
        # Create a book with special characters in title
        special_book = Book.objects.create(title="Book with <script>alert('test')</script>")
        special_book.authors.add(self.author1)
        
        # Create an author with special characters in name
        special_author = Author.objects.create(
            first_name="Mary",
            last_name="O'Connor"
        )
        special_book2 = Book.objects.create(title="Another Special Book")
        special_book2.authors.add(special_author)
        
        # Create editions with these special books
        special_edition1 = BookEdition.objects.create(
            book=special_book,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2020
        )
        
        special_edition2 = BookEdition.objects.create(
            book=special_book2,
            publisher=self.publisher2,
            series=self.series2,
            publication_year=2021
        )
        
        # Test filtering with special characters in book title
        filter_params = {'book_title': "alert"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_edition1, qs)
        
        # Test filtering with special characters in author name
        filter_params = {'author_name': "O'Connor"}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(special_edition2, qs)