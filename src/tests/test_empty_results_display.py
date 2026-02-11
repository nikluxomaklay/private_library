"""
Tests for empty results display functionality.
"""
import os
import sys
import django
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

# Add the project directory to Python path
sys.path.append('/home/saturnus/repos/private_library/src')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'private_library.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Author, Book, Publisher, BookSeries, BookEdition, Year, ReadingLog


class TestEmptyResultsDisplay(TestCase):
    """Test cases for empty results display functionality."""

    def setUp(self):
        """Set up test data for empty results tests."""
        # Create some test data
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Smith"
        )
        
        self.book1 = Book.objects.create(title="Django for Beginners")
        self.book1.authors.add(self.author1)
        
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        
        self.series1 = BookSeries.objects.create(
            name="Programming Series",
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

    def test_empty_results_on_reading_log_page(self):
        """Test empty results display on reading log page."""
        # Search for non-existent book title
        response = self.client.get(reverse('reading_log_list'), {
            'book_title': 'NonExistentBookTitle'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Записи в журнале чтения не найдены.')
        
        # Search for non-existent author name
        response = self.client.get(reverse('reading_log_list'), {
            'author_name': 'NonExistentAuthor'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Записи в журнале чтения не найдены.')

    def test_empty_results_on_authors_page(self):
        """Test empty results display on authors page."""
        # Search for non-existent author name
        response = self.client.get(reverse('author'), {
            'full_name': 'NonExistentAuthorName'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Авторы не найдены.')

    def test_empty_results_on_books_page(self):
        """Test empty results display on books page."""
        # Search for non-existent book title
        response = self.client.get(reverse('book'), {
            'title': 'NonExistentBookTitle'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Книги не найдены.')
        
        # Search for non-existent author name
        response = self.client.get(reverse('book'), {
            'author_name': 'NonExistentAuthor'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Книги не найдены.')

    def test_empty_results_on_book_editions_page(self):
        """Test empty results display on book editions page."""
        # Search for non-existent book title
        response = self.client.get(reverse('book_edition'), {
            'book_title': 'NonExistentBookTitle'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Издание книг не найдено.')
        
        # Search for non-existent publisher name
        response = self.client.get(reverse('book_edition'), {
            'publisher_name': 'NonExistentPublisher'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Издание книг не найдено.')

    def test_empty_results_on_publishers_page(self):
        """Test empty results display on publishers page."""
        # Search for non-existent publisher name
        response = self.client.get(reverse('publisher'), {
            'name': 'NonExistentPublisherName'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Издательства не найдены.')

    def test_empty_results_on_book_series_page(self):
        """Test empty results display on book series page."""
        # Search for non-existent series name
        response = self.client.get(reverse('book_series'), {
            'name': 'NonExistentSeriesName'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Серии книг не найдены.')

    def test_non_empty_results_still_show_content(self):
        """Test that non-empty results still show the content."""
        # Search for existing author name
        response = self.client.get(reverse('author'), {
            'full_name': 'John'
        })
        self.assertEqual(response.status_code, 200)
        # Should not contain the empty results message
        self.assertNotContains(response, 'Авторы не найдены.')
        # Should contain the author we created
        self.assertContains(response, 'John Smith')

    def test_empty_results_with_multiple_filters(self):
        """Test empty results when multiple filters are applied."""
        # Apply multiple filters that result in no matches
        response = self.client.get(reverse('book_edition'), {
            'book_title': 'NonExistentBook',
            'publisher_name': 'NonExistentPublisher'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Издание книг не найдено.')

    def test_empty_results_with_exact_match_filters(self):
        """Test empty results with filters that require exact matches."""
        # Search for a publication year that doesn't exist
        response = self.client.get(reverse('book_edition'), {
            'publication_year': 9999
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Издание книг не найдено.')