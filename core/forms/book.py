from dal import autocomplete
from django import forms

from core.models import Book


class BookForm(forms.ModelForm):
    def clean(self):
        return super().clean()

    class Meta:
        model = Book
        fields = (
            'title',
            'extended_title',
            'title_original',
            'extended_title_original',
            'authors',
            'publisher',
            'series',
            'publication_year',
            'isbn',
        )
        widgets = {
            'authors': autocomplete.ModelSelect2Multiple(
                url='author_autocomplete',
            ),
            'publisher': autocomplete.Select2(
                url='publisher_autocomplete',
            ),
            'series': autocomplete.Select2(
                url='book_series_autocomplete',
            ),
        }
