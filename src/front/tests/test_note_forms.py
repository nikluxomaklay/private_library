"""
Tests для форм заметок (NoteForm, NoteToBookEditionFormSet).

Тесты проверяют:
- T035: Валидация topic (required, max 255)
- T036: Блокировка циклической зависимости (parent=self)
"""
import pytest
from django.forms import ValidationError

from core.models import Note
from front.forms.notes import NoteForm, NoteToBookEditionFormSet


@pytest.mark.django_db
class TestNoteForm:
    """Тесты для NoteForm."""

    def test_note_form_requires_topic(self):
        """
        T035 [P] [US4] Validation test: note without topic fails.

        Проверяет, что:
        - Форма без topic невалидна
        - Ошибка валидации добавляется для поля topic
        """
        # Создаем форму без topic
        form = NoteForm(data={
            'topic': '',
            'text': 'Текст заметки',
            'parent': '',
            'keywords': '',
        })
        
        # Форма должна быть невалидной
        assert form.is_valid() is False, "Форма без topic должна быть невалидной"
        
        # Проверяем наличие ошибки для поля topic
        assert 'topic' in form.errors, "Должна быть ошибка для поля topic"
        
        # Проверяем, что topic required
        assert form.errors['topic'], "Ошибка topic должна быть не пустой"

    def test_note_form_topic_max_length(self):
        """
        Дополнительный тест: проверка максимальной длины topic (255 символов).

        Проверяет, что:
        - Topic длиннее 255 символов вызывает ошибку валидации
        """
        # Создаем topic длиннее 255 символов
        long_topic = 'A' * 256
        
        form = NoteForm(data={
            'topic': long_topic,
            'text': 'Текст заметки',
            'parent': '',
            'keywords': '',
        })
        
        # Форма должна быть невалидной
        assert form.is_valid() is False, "Форма с topic > 255 символов должна быть невалидной"
        
        # Проверяем наличие ошибки для поля topic
        assert 'topic' in form.errors, "Должна быть ошибка для поля topic"

    def test_note_form_valid_with_topic(self):
        """
        Дополнительный тест: форма с topic валидна.

        Проверяет, что:
        - Форма с topic валидна
        - Данные сохраняются корректно
        """
        form = NoteForm(data={
            'topic': 'Тестовая заметка',
            'text': 'Текст заметки',
            'parent': '',
            'keywords': '',
        })
        
        # Форма должна быть валидной
        assert form.is_valid() is True, f"Форма с topic должна быть валидной, ошибки: {form.errors}"
        
        # Сохраняем и проверяем
        note = form.save()
        assert note.topic == 'Тестовая заметка'
        assert note.text == 'Текст заметки'

    def test_circular_dependency_blocked(self, db):
        """
        T036 [P] [US4] Validation test: circular dependency blocked.

        Проверяет, что:
        - Попытка установить parent=self блокируется
        - Ошибка валидации добавляется для поля parent
        """
        # Создаем заметку
        note = Note.objects.create(
            index='1',
            topic='Тестовая заметка',
            text='Текст заметки'
        )
        
        # Пытаемся обновить заметку с parent=self
        form = NoteForm(
            data={
                'topic': 'Обновленная заметка',
                'text': 'Обновленный текст',
                'parent': str(note.pk),  # Пытаемся установить parent=self
                'keywords': '',
            },
            instance=note
        )
        
        # Форма должна быть невалидной
        assert form.is_valid() is False, "Форма с parent=self должна быть невалидной"
        
        # Проверяем наличие ошибки для поля parent
        assert 'parent' in form.errors, "Должна быть ошибка для поля parent"
        
        # Проверяем текст ошибки
        error_message = str(form.errors['parent'])
        assert 'циклическую' in error_message.lower() or 'circular' in error_message.lower(), \
            f"Ошибка должна упоминать циклическую зависимость, получено: {error_message}"

    def test_circular_dependency_child_parent(self, db):
        """
        Дополнительный тест: проверка на циклическую зависимость в иерархии.

        Проверяет, что:
        - Нельзя установить parent потомком своей дочерней заметки
        """
        # Создаем иерархию: parent -> child
        parent = Note.objects.create(
            index='1',
            topic='Родительская заметка',
            text='Текст родителя'
        )
        child = Note.objects.create(
            index='1.1',
            topic='Дочерняя заметка',
            text='Текст ребенка',
            parent=parent
        )
        
        # Пытаемся установить parent=child для parent (создать цикл)
        form = NoteForm(
            data={
                'topic': 'Обновленная родительская заметка',
                'text': 'Обновленный текст',
                'parent': str(child.pk),  # Пытаемся сделать child родителем parent
                'keywords': '',
            },
            instance=parent
        )
        
        # Форма должна быть невалидной
        assert form.is_valid() is False, "Форма с циклической зависимостью должна быть невалидной"
        
        # Проверяем наличие ошибки для поля parent
        assert 'parent' in form.errors, "Должна быть ошибка для поля parent"


@pytest.mark.django_db
class TestNoteToBookEditionFormSet:
    """Тесты для NoteToBookEditionFormSet."""

    def test_formset_empty_elements_filtered(self, db, book_editions):
        """
        Дополнительный тест: пустые элементы formset игнорируются.

        Проверяет, что:
        - Формы без book_edition игнорируются при сохранении
        """
        from django.forms import formset_factory
        
        # Создаем заметку
        note = Note.objects.create(
            index='1',
            topic='Тестовая заметка',
            text='Текст заметки'
        )
        
        # Создаем formset с одной заполненной и одной пустой формой
        formset = NoteToBookEditionFormSet(data={
            'book_editions-TOTAL_FORMS': '2',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': str(book_editions[0].pk),
            'book_editions-0-additional_info': 'Информация 1',
            'book_editions-0-DELETE': '',
            'book_editions-1-book_edition': '',  # Пустая форма
            'book_editions-1-additional_info': '',
            'book_editions-1-DELETE': '',
        })
        
        # Formset должен быть валидным
        assert formset.is_valid() is True, f"Formset должен быть валидным, ошибки: {formset.errors}"
        
        # Сохраняем formset
        formset.instance = note
        formset.save()
        
        # Проверяем, что сохранена только одна связь (с book_edition)
        assert note.book_editions.count() == 1, \
            f"Должна быть 1 связь, найдено: {note.book_editions.count()}"

    def test_formset_additional_info_disabled_without_book(self):
        """
        Дополнительный тест: additional_info без book_edition не сохраняется.

        Проверяет, что:
        - additional_info без выбранного book_edition игнорируется
        """
        # Создаем заметку
        note = Note.objects.create(
            index='1',
            topic='Тестовая заметка',
            text='Текст заметки'
        )
        
        # Создаем formset с additional_info но без book_edition
        formset = NoteToBookEditionFormSet(data={
            'book_editions-TOTAL_FORMS': '1',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': '',  # Нет book_edition
            'book_editions-0-additional_info': 'Информация без книги',
            'book_editions-0-DELETE': '',
        })
        
        # Formset должен быть валидным (пустые формы игнорируются)
        assert formset.is_valid() is True, f"Formset должен быть валидным, ошибки: {formset.errors}"
        
        # Сохраняем formset
        formset.instance = note
        formset.save()
        
        # Проверяем, что связей нет
        assert note.book_editions.count() == 0, \
            f"Не должно быть связей без book_edition, найдено: {note.book_editions.count()}"


@pytest.fixture
def book_editions(db):
    """
    Создает тестовые book_editions для тестирования.
    """
    from core.models import Book, Publisher, BookEdition
    
    # Создаем книги и издательства
    publisher = Publisher.objects.create(name='Тестовое издательство')
    
    books = []
    for i in range(3):
        book = Book.objects.create(title=f'Книга {i+1}')
        books.append(book)
    
    # Создаем book_editions
    editions = []
    for i, book in enumerate(books):
        edition = BookEdition.objects.create(
            book=book,
            publisher=publisher,
            publication_year=2024 + i,
            edition_type='PAPER_BOOK'
        )
        editions.append(edition)
    
    return editions
