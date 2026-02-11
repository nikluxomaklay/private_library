"""
Tests for partial matching functionality in all 'поиск по подстроке' fields.
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


class TestPartialMatching(TestCase):
    """Test cases for partial matching functionality in all 'поиск по подстроке' fields."""

    def setUp(self):
        """Set up test data for partial matching tests."""
        # Create test data with various names for partial matching
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Smith"
        )
        
        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Johnson"
        )
        
        self.author3 = Author.objects.create(
            first_name="Robert",
            last_name="Williams"
        )
        
        self.book1 = Book.objects.create(title="Django for Beginners")
        self.book1.authors.add(self.author1)
        
        self.book2 = Book.objects.create(title="Python Tricks")
        self.book2.authors.add(self.author2)
        
        self.book3 = Book.objects.create(title="Advanced Python Programming")
        self.book3.authors.add(self.author3)
        
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        self.publisher2 = Publisher.objects.create(name="Programming Press")
        
        self.series1 = BookSeries.objects.create(
            name="Programming Series",
            publisher=self.publisher1
        )
        self.series2 = BookSeries.objects.create(
            name="Web Development Series",
            publisher=self.publisher2
        )
        
        self.year_2020 = Year.objects.create(year=2020)
        self.year_2021 = Year.objects.create(year=2021)
        
        self.book_edition1 = BookEdition.objects.create(
            book=self.book1,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2020
        )
        
        self.book_edition2 = BookEdition.objects.create(
            book=self.book2,
            publisher=self.publisher2,
            series=self.series2,
            publication_year=2021
        )
        
        self.reading_log1 = ReadingLog.objects.create(
            book_edition=self.book_edition1,
            year_start=self.year_2020,
            month_start=3,
            year_finish=self.year_2020,
            month_finish=6
        )
        
        self.reading_log2 = ReadingLog.objects.create(
            book_edition=self.book_edition2,
            year_start=self.year_2021,
            month_start=1,
            year_finish=self.year_2021,
            month_finish=12
        )

    def test_reading_log_partial_matching(self):
        """Test partial matching in ReadingLog filter."""
        # Test partial book title matching
        filter_params = {'book_title': 'Django'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)  # Contains "Django for Beginners"
        self.assertNotIn(self.reading_log2, qs)  # Does not contain "Django"
        
        # Test partial author name matching
        filter_params = {'author_name': 'Smith'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)  # Book by John Smith
        self.assertNotIn(self.reading_log2, qs)  # Book by Jane Johnson
        
        # Test partial publisher name matching
        filter_params = {'publisher_name': 'Tech'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)  # Published by Tech Publications
        self.assertNotIn(self.reading_log2, qs)  # Published by Programming Press
        
        # Test partial series name matching
        filter_params = {'book_series_name': 'Programming'}
        filter_set = ReadingLogFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.reading_log1, qs)  # Part of Programming Series
        self.assertNotIn(self.reading_log2, qs)  # Part of Web Development Series

    def test_author_partial_matching(self):
        """Test partial matching in Author filter."""
        # Test partial name matching
        filter_params = {'full_name': 'John'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)  # John Smith
        self.assertIn(self.author2, qs)  # Jane Johnson (contains 'John')
        self.assertNotIn(self.author3, qs)  # Robert Williams
        
        # Test another partial match
        filter_params = {'full_name': 'Will'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.author1, qs)  # John Smith
        self.assertNotIn(self.author2, qs)  # Jane Johnson
        self.assertIn(self.author3, qs)  # Robert Williams (contains 'Will')

    def test_book_partial_matching(self):
        """Test partial matching in Book filter."""
        # Test partial title matching
        filter_params = {'title': 'Python'}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.book1, qs)  # Django for Beginners
        self.assertIn(self.book2, qs)  # Python Tricks
        self.assertIn(self.book3, qs)  # Advanced Python Programming
        
        # Test partial author name matching
        filter_params = {'author_name': 'Jane'}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.book1, qs)  # By John Smith
        self.assertIn(self.book2, qs)  # By Jane Johnson
        self.assertNotIn(self.book3, qs)  # By Robert Williams

    def test_book_edition_partial_matching(self):
        """Test partial matching in BookEdition filter."""
        # Test partial book title matching
        filter_params = {'book_title': 'Django'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book_edition1, qs)  # Book "Django for Beginners"
        self.assertNotIn(self.book_edition2, qs)  # Book "Python Tricks"
        
        # Test partial author name matching
        filter_params = {'author_name': 'Smith'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book_edition1, qs)  # Book by John Smith
        self.assertNotIn(self.book_edition2, qs)  # Book by Jane Johnson
        
        # Test partial publisher name matching
        filter_params = {'publisher_name': 'Press'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.book_edition1, qs)  # Published by Tech Publications
        self.assertIn(self.book_edition2, qs)  # Published by Programming Press
        
        # Test partial series name matching
        filter_params = {'book_series_name': 'Web'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.book_edition1, qs)  # Part of Programming Series
        self.assertIn(self.book_edition2, qs)  # Part of Web Development Series

    def test_publisher_partial_matching(self):
        """Test partial matching in Publisher filter."""
        # Test partial name matching
        filter_params = {'name': 'Tech'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.publisher1, qs)  # Tech Publications
        self.assertNotIn(self.publisher2, qs)  # Programming Press
        
        # Test another partial match
        filter_params = {'name': 'Program'}
        filter_set = PublisherFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.publisher1, qs)  # Tech Publications
        self.assertIn(self.publisher2, qs)  # Programming Press (contains 'Program')

    def test_book_series_partial_matching(self):
        """Test partial matching in BookSeries filter."""
        # Test partial name matching
        filter_params = {'name': 'Programming'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.series1, qs)  # Programming Series
        self.assertNotIn(self.series2, qs)  # Web Development Series
        
        # Test another partial match
        filter_params = {'name': 'Development'}
        filter_set = BookSeriesFilter(data=filter_params)
        qs = filter_set.qs
        self.assertNotIn(self.series1, qs)  # Programming Series
        self.assertIn(self.series2, qs)  # Web Development Series (contains 'Development')

    def test_case_insensitive_partial_matching(self):
        """Test that partial matching is case insensitive."""
        # Test with lowercase
        filter_params = {'title': 'django'}
        filter_set = BookFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.book1, qs)  # "Django for Beginners" should match "django"
        
        # Test with mixed case
        filter_params = {'full_name': 'SMITH'}
        filter_set = AuthorFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(self.author1, qs)  # "John Smith" should match "SMITH"

    def test_middle_string_partial_matching(self):
        """Test that partial matching works with substrings in the middle of strings."""
        # Create a book with a title that has a searchable substring in the middle
        middle_book = Book.objects.create(title="Learning Advanced Django Techniques")
        middle_book.authors.add(self.author1)
        
        middle_edition = BookEdition.objects.create(
            book=middle_book,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2020
        )
        
        # Search for the middle substring
        filter_params = {'book_title': 'Advanced'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(middle_edition, qs)  # Should match "Learning Advanced Django Techniques"

    def test_whitespace_handling_in_partial_matching(self):
        """Test that partial matching handles whitespace properly."""
        # Create a book with spaces and special characters
        spaced_book = Book.objects.create(title="  Django   for   Beginners  ")
        spaced_book.authors.add(self.author1)
        
        spaced_edition = BookEdition.objects.create(
            book=spaced_book,
            publisher=self.publisher1,
            series=self.series1,
            publication_year=2020
        )
        
        # Search for parts of the title with different spacing
        filter_params = {'book_title': 'for'}
        filter_set = BookEditionFilter(data=filter_params)
        qs = filter_set.qs
        self.assertIn(spaced_edition, qs)  # Should match despite extra whitespace