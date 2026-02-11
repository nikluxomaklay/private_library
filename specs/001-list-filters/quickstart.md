# Quickstart Guide: List Filters

## Overview
This guide explains how to implement and use the filtering functionality for the 6 list pages in the private library application using django-filter.

## Prerequisites
- Python 3.11+
- Django 4.x
- django-bootstrap5
- django-autocomplete-light (for dynamic selectors)
- django-filter
- PostgreSQL database

## Implementation Steps

### 1. Create FilterSet Classes
Create filter classes in `books/filters.py` for each list page using django-filter:

```python
# Example for book filtering
import django_filters
from dal import autocomplete
from django import forms
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Название книги',
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию книги',
            'class': 'form-control'
        })
    )
    
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        widget=autocomplete.TagSelect2(
            url='author-autocomplete',
            forward=['title'],
            attrs={'class': 'form-control'}
        ),
        label='Автор'
    )

    class Meta:
        model = Book
        fields = ['title', 'author']
```

### 2. Update Views
Modify list views in `books/views.py` to use the FilterSet:

```python
from django_filters.views import FilterView
from .filters import BookFilter

class BookListView(FilterView):
    model = Book
    filterset_class = BookFilter
    template_name = 'book_list.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context
```

### 3. Update Templates
Add filter forms to list templates, maintaining the same styling as existing content addition pages:

```html
<!-- In book_list.html -->
<form method="GET" class="mb-4">
    <div class="row">
        <div class="col-md-4">
            {{ filter.form.title.label_tag }}
            {{ filter.form.title }}
        </div>
        <div class="col-md-4">
            {{ filter.form.author.label_tag }}
            {{ filter.form.author }}
        </div>
        <div class="col-md-4 d-flex align-items-end">
            <button type="submit" class="btn btn-primary">Фильтровать</button>
            <a href="{% url 'book-list' %}" class="btn btn-secondary ms-2">Сбросить</a>
        </div>
    </div>
</form>

<!-- Display filtered results -->
{% for book in filter.qs %}
    <!-- Render book details -->
{% empty %}
    <p>Книги не найдены.</p>
{% endfor %}
```

### 4. Configure URLs
Add URL patterns in `books/urls.py`:

```python
from django.urls import path
from .views import BookListView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    # Other filter URLs...
]
```

### 5. Add Autocomplete URLs (if needed)
For dynamic selectors that pull data from the database:

```python
# In books/urls.py
path('author-autocomplete/', AuthorAutocomplete.as_view(), name='author-autocomplete'),
```

## Special Filter Types

### Year/Month Selectors
For reading log filters that require year and month selectors:

```python
import django_filters
from .models import ReadingLog

class ReadingLogFilter(django_filters.FilterSet):
    YEAR_CHOICES = [(year, str(year)) for year in range(2000, 2030)]
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    year_from = django_filters.ChoiceFilter(
        choices=YEAR_CHOICES,
        field_name='publication_year',
        lookup_expr='gte',
        label='Год от'
    )
    
    year_to = django_filters.ChoiceFilter(
        choices=YEAR_CHOICES,
        field_name='publication_year',
        lookup_expr='lte',
        label='Год до'
    )
    
    month_from = django_filters.ChoiceFilter(
        choices=MONTH_CHOICES,
        field_name='reading_date__month',
        lookup_expr='gte',
        label='Месяц от'
    )
    
    month_to = django_filters.ChoiceFilter(
        choices=MONTH_CHOICES,
        field_name='reading_date__month',
        lookup_expr='lte',
        label='Месяц до'
    )
```

### Exact Match Filters
For publication year exact match:

```python
publication_year = django_filters.NumberFilter(
    field_name='publication_year',
    lookup_expr='exact',
    label='Год издания'
)
```

## Testing
Write tests to verify filter functionality:

```python
def test_book_filter_by_title():
    # Create test data
    Book.objects.create(title="Django for Beginners")
    
    # Create filter
    filter = BookFilter(data={'title': 'Django'})
    
    # Verify filtering works
    assert len(filter.qs) == 1
    assert filter.qs.first().title == "Django for Beginners"
```

## Performance Considerations
- Add database indexes on frequently filtered fields
- Implement pagination for large result sets
- Use select_related/prefetch_related to minimize database queries
- Leverage django-filter's optimization features