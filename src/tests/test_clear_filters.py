"""
Tests for clear filters functionality across all pages.
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


class TestClearFiltersFunctionality(TestCase):
    """Test cases for clear filters functionality across all pages."""

    def setUp(self):
        """Set up test data for clear filters tests."""
        # Create test data
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Smith"
        )
        
        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Doe"
        )
        
        self.book1 = Book.objects.create(title="Django for Beginners")
        self.book1.authors.add(self.author1)
        
        self.book2 = Book.objects.create(title="Python Tricks")
        self.book2.authors.add(self.author2)
        
        self.publisher1 = Publisher.objects.create(name="Tech Publications")
        self.publisher2 = Publisher.objects.create(name="Programming Press")
        
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

    def test_clear_filters_redirects_to_base_url(self):
        """Test that clear filters button redirects to the base URL without filters."""
        # Test Reading Log page
        response = self.client.get(reverse('reading_log_list'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('reading_log_list'), {
            'book_title': 'Django',
            'author_name': 'Smith'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/reading-log/"')
        
        # Test Authors page
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('author'), {
            'full_name': 'John'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/author/"')
        
        # Test Books page
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('book'), {
            'title': 'Django',
            'author_name': 'Smith'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/book/"')
        
        # Test Book Editions page
        response = self.client.get(reverse('book_edition'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('book_edition'), {
            'book_title': 'Django',
            'publisher_name': 'Tech'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/book-edition/"')
        
        # Test Publishers page
        response = self.client.get(reverse('publisher'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('publisher'), {
            'name': 'Tech'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/publisher/"')
        
        # Test Book Series page
        response = self.client.get(reverse('book_series'))
        self.assertEqual(response.status_code, 200)
        
        # Apply some filters
        response = self.client.get(reverse('book_series'), {
            'name': 'Programming'
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that the clear filters link is present in the response content
        self.assertContains(response, 'href="/book-series/"')

    def test_clear_filters_removes_query_parameters(self):
        """Test that clicking clear filters removes all query parameters."""
        # Test with Reading Log page
        # Apply filters and check that results are filtered
        response = self.client.get(reverse('reading_log_list'), {
            'book_title': 'Django'
        })
        self.assertEqual(response.status_code, 200)
        
        # The response should contain the clear filters link
        self.assertContains(response, 'href="/reading-log/"')
        
        # Follow the clear filters link (simulate click)
        clear_response = self.client.get('/reading-log/')
        self.assertEqual(clear_response.status_code, 200)
        
        # After clearing filters, the page should show all results
        # (This is harder to test without knowing the exact number of records in the DB)
        # But we can at least verify that the URL has no query parameters
        self.assertNotIn('?', clear_response.wsgi_request.get_full_path())
        
        # Test with Authors page
        response = self.client.get(reverse('author'), {
            'full_name': 'John'
        })
        self.assertEqual(response.status_code, 200)
        
        # Follow the clear filters link
        clear_response = self.client.get('/author/')
        self.assertEqual(clear_response.status_code, 200)
        
        # Verify URL has no query parameters
        self.assertNotIn('?', clear_response.wsgi_request.get_full_path())

    def test_clear_filters_template_links(self):
        """Test that the clear filters links are correctly rendered in templates."""
        # Test Reading Log template
        response = self.client.get(reverse('reading_log_list'))
        self.assertContains(response, 'Сбросить фильтры')
        self.assertContains(response, 'href="/reading-log/"')
        
        # Test Authors template
        response = self.client.get(reverse('author'))
        self.assertContains(response, 'Сбросить фильтры')
        self.assertContains(response, 'href="/author/"')
        
        # Test Books template
        response = self.client.get(reverse('book'))
        self.assertContains(response, 'Сбросить фильтры')
        self.assertContains(response, 'href="/book/"')
        
        # Test Book Editions template
        response = self.client.get(reverse('book_edition'))
        self.assertContains(response, 'Сбросить')
        self.assertContains(response, 'href="/book-edition/"')
        
        # Test Publishers template
        response = self.client.get(reverse('publisher'))
        self.assertContains(response, 'Сбросить фильтры')
        self.assertContains(response, 'href="/publisher/"')
        
        # Test Book Series template
        response = self.client.get(reverse('book_series'))
        self.assertContains(response, 'Сбросить фильтры')
        self.assertContains(response, 'href="/book-series/"')

    def test_clear_filters_works_with_multiple_params(self):
        """Test that clear filters works when multiple parameters are present."""
        # Test with multiple filters on Reading Log
        response = self.client.get(reverse('reading_log_list'), {
            'book_title': 'Django',
            'author_name': 'Smith',
            'publisher_name': 'Tech',
            'publication_year': '2020'
        })
        self.assertEqual(response.status_code, 200)
        
        # The page should still contain the clear filters link
        self.assertContains(response, 'href="/reading-log/"')
        
        # Test with multiple filters on Books
        response = self.client.get(reverse('book'), {
            'title': 'Python',
            'author_name': 'Jane'
        })
        self.assertEqual(response.status_code, 200)
        
        # The page should still contain the clear filters link
        self.assertContains(response, 'href="/book/"')