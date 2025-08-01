from dal import autocomplete
from django import forms

from core.models import Book
from core.models import BookEdition


class BookEditionNewForm(forms.ModelForm):
    class Meta:
        model = BookEdition
        fields = (
            'book',
            'publisher',
            'series',
            'publication_year',
            'isbn',
        )
        widgets = {
            'book': autocomplete.Select2(
                url='book_autocomplete',
                attrs={"data-theme": "bootstrap-5"}
            ),
            'publisher': autocomplete.Select2(
                url='publisher_autocomplete',
                attrs={"data-theme": "bootstrap-5"}
            ),
            'series': autocomplete.Select2(
                url='book_series_autocomplete',
                attrs={"data-theme": "bootstrap-5"}
            ),
        }


class BookEditionUpdateForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects,
        disabled=True,
    )

    class Meta:
        model = BookEdition
        fields = (
            'book',
            'publisher',
            'series',
            'publication_year',
            'isbn',
        )
        read_only = ('book',)
        widgets = {
            'publisher': autocomplete.Select2(
                url='publisher_autocomplete',
                attrs={"data-theme": "bootstrap-5"}
            ),
            'series': autocomplete.Select2(
                url='book_series_autocomplete',
                attrs={"data-theme": "bootstrap-5"}
            ),
        }
