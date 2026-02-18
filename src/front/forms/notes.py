"""
Формы для работы с заметками (Note) и связями с изданиями книг (NoteToBookEdition).

Этот модуль содержит:
- NoteForm: форма для создания и редактирования заметок
- NoteToBookEditionFormSet: inline formset для связи заметок с изданиями книг
"""

from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from core.models import Note, NoteToBookEdition


class NoteForm(forms.ModelForm):
    """
    ModelForm для модели Note.

    Поля:
    - topic: тема заметки (обязательное, макс. 255 символов)
    - text: текст заметки (необязательное)
    - parent: родительская заметка (autocomplete)
    - keywords: ключевые слова (autocomplete, множественный выбор, необязательное)
    """

    class Meta:
        model = Note
        fields = ('topic', 'text', 'parent', 'keywords')
        widgets = {
            'parent': autocomplete.ModelSelect2(
                url='note_autocomplete',
                attrs={
                    'data-theme': 'bootstrap-5',
                    'data-placeholder': 'Выберите родительскую заметку...',
                    'data-allow-clear': 'true',
                }
            ),
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete',
                attrs={
                    'data-theme': 'bootstrap-5',
                    'data-placeholder': 'Выберите ключевые слова...',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.

        Делает поле keywords необязательным (required=False).
        Обрабатывает keywords_initial для pre-fill из parent note.
        """
        super().__init__(*args, **kwargs)
        self.fields['keywords'].required = False
        
        # Обработка keywords_initial для pre-fill из parent note
        keywords_initial = kwargs.get('initial', {}).get('keywords_initial')
        if keywords_initial and not self.is_bound:
            self.fields['keywords'].initial = keywords_initial

    def clean_topic(self):
        """
        Валидация поля topic.

        Проверяет:
        - topic обязателен (не пустой)
        - topic не длиннее 255 символов
        """
        topic = self.cleaned_data.get('topic')
        if not topic:
            raise ValidationError(_('Поле "Тема" обязательно для заполнения.'))
        if len(topic) > 255:
            raise ValidationError(_('Тема не должна превышать 255 символов.'))
        return topic

    def clean_parent(self):
        """
        Валидация поля parent на циклическую зависимость.

        Проверяет:
        - parent != self (нельзя быть родителем самому себе)
        - parent не является потомком self (нельзя создать цикл в иерархии)
        """
        parent = self.cleaned_data.get('parent')
        
        # Если у нас есть существующий экземпляр (редактирование)
        if self.instance.pk and parent:
            # Проверка: parent != self
            if parent.id == self.instance.id:
                raise ValidationError(
                    _('Нельзя создать циклическую зависимость: заметка не может быть родителем самой себя.')
                )
            
            # Проверка: parent не является потомком self
            # Используем рекурсивную проверку через children
            if self._is_descendant(parent, self.instance):
                raise ValidationError(
                    _('Нельзя создать циклическую зависимость: родительская заметка не может быть потомком текущей.')
                )
        
        return parent

    def _is_descendant(self, potential_descendant, potential_ancestor):
        """
        Проверяет, является ли potential_descendant потомком potential_ancestor.

        Рекурсивно проверяет иерархию заметок.
        """
        # Базовый случай: если potential_descendant не имеет родителя
        if not potential_descendant:
            return False
        
        # Если нашли direct parent
        if potential_descendant.parent == potential_ancestor:
            return True
        
        # Рекурсивно проверяем родителя potential_descendant
        if potential_descendant.parent:
            return self._is_descendant(potential_descendant.parent, potential_ancestor)

        return False


class NoteToBookEditionFormSetClass(forms.BaseInlineFormSet):
    """
    Custom inline formset для связи Note с BookEdition.

    Переопределяет clean() для фильтрации пустых элементов:
    - Игнорирует формы без выбранного book_edition
    - additional_info без book_edition не сохраняется
    """

    def clean(self):
        """
        Валидация formset с фильтрацией пустых элементов.

        Игнорирует формы без book_edition, позволяя иметь дополнительные
        пустые формы в formset.
        """
        super().clean()
        
        # Фильтруем пустые элементы (без book_edition)
        # Это позволяет иметь дополнительные формы в formset без ошибок
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            
            # Если book_edition не выбран, помечаем форму на удаление
            # Это предотвратит сохранение пустых форм
            book_edition = form.cleaned_data.get('book_edition')
            if not book_edition:
                # Помечаем форму как требующую удаления
                # Это безопасно даже для новых форм
                form.cleaned_data['DELETE'] = True


# Inline formset для связи Note с BookEdition
NoteToBookEditionFormSet = inlineformset_factory(
    parent_model=Note,
    model=NoteToBookEdition,
    fields=('id', 'book_edition', 'additional_info'),
    formset=NoteToBookEditionFormSetClass,
    widgets={
        'book_edition': autocomplete.ModelSelect2(
            url='book_edition_autocomplete',
            attrs={
                'data-theme': 'bootstrap-5',
                'data-placeholder': 'Выберите издание книги...',
                'data-allow-clear': 'true',
            }
        ),
    },
    validate_min=False,
    validate_max=False,
    can_delete=True,
    extra=1,
)
