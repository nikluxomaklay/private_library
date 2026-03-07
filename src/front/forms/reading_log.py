from django import forms
from core.models import ReadingLog


class ReadingLogForm(forms.ModelForm):
    """Форма для редактирования ReadingLog."""

    class Meta:
        model = ReadingLog
        fields = [
            'year_start',
            'month_start',
            'year_finish',
            'month_finish',
        ]

    def clean(self):
        """
        Валидация: дата окончания не может быть раньше даты начала.
        """
        cleaned_data = super().clean()
        year_start = cleaned_data.get('year_start')
        year_finish = cleaned_data.get('year_finish')
        month_start = cleaned_data.get('month_start')
        month_finish = cleaned_data.get('month_finish')

        if year_start and year_finish:
            # Сравниваем значения year у объектов Year
            if year_finish.year < year_start.year:
                raise forms.ValidationError(
                    "Год окончания не может быть раньше года начала"
                )
            elif year_finish.year == year_start.year and month_finish and month_start:
                if month_finish < month_start:
                    raise forms.ValidationError(
                        "Месяц окончания не может быть раньше месяца начала "
                        "в пределах одного года"
                    )

        return cleaned_data
