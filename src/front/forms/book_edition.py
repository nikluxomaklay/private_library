from dal import autocomplete
from django import forms

from core.models import Book
from core.models import BookEdition


class BookEditionNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for edition_type if not already set
        if not self.instance.pk:  # Only for new instances
            if not self.initial.get('edition_type'):
                self.initial['edition_type'] = 'PAPER_BOOK'

    class Meta:
        model = BookEdition
        fields = (
            'book',
            'publisher',
            'series',
            'publication_year',
            'isbn',
            'edition_type',
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
            'edition_type': forms.Select(attrs={"class": "form-select"}),
        }


class BookEditionUpdateForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects,
        disabled=True,
    )
    edition_type = forms.ChoiceField(
        choices=BookEdition.EDITION_TYPE_CHOICES,
        disabled=True,  # Make the field read-only to enforce immutability
    )

    class Meta:
        model = BookEdition
        fields = (
            'book',
            'publisher',
            'series',
            'publication_year',
            'isbn',
            'edition_type',
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
            'edition_type': forms.Select(attrs={"class": "form-select", "readonly": "readonly"}),
        }
