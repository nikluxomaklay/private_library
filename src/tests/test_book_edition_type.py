from django.test import TestCase
from core.models import Book, Author, BookEdition


class BookEditionTypeTestCase(TestCase):
    def setUp(self):
        # Create a test author
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author"
        )
        
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book"
        )
        self.book.authors.add(self.author)
        
    def test_book_edition_type_creation(self):
        """Test that book editions can be created with edition type"""
        book_edition = BookEdition.objects.create(
            book=self.book,
            edition_type='EBOOK'  # Use EBOOK type for testing
        )
        
        self.assertEqual(book_edition.edition_type, 'EBOOK')
        self.assertEqual(str(book_edition), "Test Book - EBOOK")  # This might fail due to __str__ method
    
    def test_book_edition_type_default(self):
        """Test that book editions get default edition type when not specified"""
        # Create a book edition without specifying edition_type
        # The default should be 'PAPER_BOOK' due to model definition
        book_edition = BookEdition.objects.create(
            book=self.book
        )
        
        self.assertEqual(book_edition.edition_type, 'PAPER_BOOK')
        
    def test_book_edition_type_choices(self):
        """Test that edition type choices are properly defined"""
        choices = dict(BookEdition.EDITION_TYPE_CHOICES)
        
        expected_choices = {
            'PAPER_BOOK': 'Paper Book',
            'EBOOK': 'E-book',
            'AUDIOBOOK': 'Audiobook',
            'WEBPAGE': 'Web Page',
        }
        
        self.assertEqual(choices, expected_choices)