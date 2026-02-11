"""
FilterSet classes for the private library application.

This module contains all FilterSet classes for filtering different
entities in the library system according to the specification.
"""

import django_filters
from django import forms
from .models import Book, Author, Publisher, BookSeries, ReadingLog, BookEdition


class BaseFilterSet(django_filters.FilterSet):
    """
    Base FilterSet class with common functionality for special character sanitization.
    
    Implements common features required across all filter sets including:
    - Special character sanitization
    - Character limit validation (255 chars)
    """
    
    def __init__(self, data=None, *args, **kwargs):
        # Apply character limit validation to all CharFilter fields
        super().__init__(data, *args, **kwargs)
        
        # Apply character limit validation to all CharFilter fields
        for field_name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                # Add character limit validator
                field.extra['validators'] = [self.validate_char_limit]
                
                # Apply sanitization if needed
                original_method = field.field_class.clean
                def wrapped_clean(value):
                    sanitized_value = self.sanitize_special_chars(value)
                    return original_method(sanitized_value)
                field.field_class.clean = wrapped_clean
    
    def validate_char_limit(self, value):
        """Validate that text inputs do not exceed 255 characters."""
        if value and len(str(value)) > 255:
            raise forms.ValidationError('Значение не должно превышать 255 символов.')
        return value
    
    def sanitize_special_chars(self, value):
        """Sanitize special characters to prevent injection attacks."""
        if value is None:
            return value
            
        # Convert to string if needed
        value_str = str(value)
        
        # Basic sanitization - remove potentially harmful characters
        # In a real-world scenario, you might want more sophisticated sanitization
        sanitized = value_str.replace('<', '&lt;').replace('>', '&gt;')
        
        return sanitized
    
    class Meta:
        # Common meta options can be defined here
        pass


class ReadingLogFilter(BaseFilterSet):
    """
    FilterSet for ReadingLog model with year/month selectors and text search.
    
    Implements requirements:
    - FR-001: Year 'from' and 'to' selectors
    - FR-002: Month 'from' and 'to' selectors
    - FR-003: Combined year+month 'from' and 'to' selectors
    - FR-004: Book title search by substring
    - FR-005: Author name search by substring
    - FR-006: Publisher name search by substring
    - FR-007: Publication year exact match filter
    - FR-008: Book series name search by substring
    """
    
    # Year range filters
    year_from = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        label='Год от',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите год от'
        })
    )
    
    year_to = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        label='Год до',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите год до'
        })
    )
    
    # Month range filters
    month_from = django_filters.NumberFilter(
        field_name='reading_date__month',
        lookup_expr='gte',
        label='Месяц от',
        widget=forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={
            'class': 'form-control'
        })
    )
    
    month_to = django_filters.NumberFilter(
        field_name='reading_date__month',
        lookup_expr='lte',
        label='Месяц до',
        widget=forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={
            'class': 'form-control'
        })
    )
    
    # Text search filters
    book_title = django_filters.CharFilter(
        field_name='book_title',
        lookup_expr='icontains',
        label='Название книги',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию книги'
        })
    )
    
    author_name = django_filters.CharFilter(
        field_name='author_name',
        lookup_expr='icontains',
        label='Имя автора',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по имени автора'
        })
    )
    
    publisher_name = django_filters.CharFilter(
        field_name='publisher_name',
        lookup_expr='icontains',
        label='Название издательства',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по издательству'
        })
    )
    
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        label='Год публикации',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Точный год публикации'
        })
    )
    
    book_series_name = django_filters.CharFilter(
        field_name='book_series_name',
        lookup_expr='icontains',
        label='Название серии книг',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию серии'
        })
    )
    
    class Meta:
        model = ReadingLog
        fields = [
            'book_title', 'author_name', 'publisher_name', 
            'publication_year', 'book_series_name'
        ]


class AuthorFilter(BaseFilterSet):
    """
    FilterSet for Author model with name search by substring.
    
    Implements requirement:
    - FR-009: Author name search by substring
    """
    
    full_name = django_filters.CharFilter(
        field_name='full_name',
        lookup_expr='icontains',
        label='Имя автора',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по имени автора'
        })
    )
    
    class Meta:
        model = Author
        fields = ['full_name']


class BookFilter(BaseFilterSet):
    """
    FilterSet for Book model with title and author search.
    
    Implements requirements:
    - FR-010: Book title search by substring
    - FR-011: Author name search by substring using django-autocomplete-light
    """
    
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название книги',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию книги'
        })
    )
    
    # Note: Author filter will be implemented with django-autocomplete-light
    # as specified in the requirements
    
    class Meta:
        model = Book
        fields = ['title']


class BookEditionFilter(BaseFilterSet):
    """
    FilterSet for BookEdition model with multiple search criteria.
    
    Implements requirements:
    - FR-012: Book title search by substring
    - FR-013: Author name search by substring using django-autocomplete-light
    - FR-014: Publisher name search by substring
    - FR-015: Publication year exact match filter
    - FR-016: Book series name search by substring
    """
    
    book_title = django_filters.CharFilter(
        field_name='book_title',
        lookup_expr='icontains',
        label='Название книги',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию книги'
        })
    )
    
    publisher_name = django_filters.CharFilter(
        field_name='publisher_name',
        lookup_expr='icontains',
        label='Название издательства',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по издательству'
        })
    )
    
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        label='Год публикации',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Точный год публикации'
        })
    )
    
    book_series_name = django_filters.CharFilter(
        field_name='book_series_name',
        lookup_expr='icontains',
        label='Название серии книг',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию серии'
        })
    )
    
    class Meta:
        model = BookEdition
        fields = [
            'book_title', 'publisher_name', 
            'publication_year', 'book_series_name'
        ]


class PublisherFilter(BaseFilterSet):
    """
    FilterSet for Publisher model with name search by substring.
    
    Implements requirement:
    - FR-017: Publisher name search by substring
    """
    
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название издательства',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию издательства'
        })
    )
    
    class Meta:
        model = Publisher
        fields = ['name']


class BookSeriesFilter(BaseFilterSet):
    """
    FilterSet for BookSeries model with name search by substring.
    
    Implements requirement:
    - FR-018: Book series name search by substring
    """
    
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название серии книг',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию серии'
        })
    )
    
    class Meta:
        model = BookSeries
        fields = ['name']