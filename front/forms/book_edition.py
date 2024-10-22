from dal import autocomplete
from django import forms

from core.models import BookEdition


class BookEditionForm(forms.ModelForm):
    def clean(self):
        return super().clean()

    class Meta:
        model = BookEdition
        fields = (
            'book',
            'publisher',
            'series',
        )
        widgets = {
            'book': autocomplete.ModelSelect2Multiple(
                url='book_autocomplete',
            ),
            'publisher': autocomplete.Select2(
                url='publisher_autocomplete',
            ),
            'series': autocomplete.Select2(
                url='book_series_autocomplete',
            ),
        }
