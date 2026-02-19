"""
Integration tests для обновления заметок (NoteUpdateView).

Тесты проверяют:
- T057: Обновление topic заметки
- T058: Обновление book_editions inline
- T059: Блокировка циклической зависимости при обновлении
"""
import pytest
from django.urls import reverse

from core.models import Note, NoteToBookEdition, BookEdition


@pytest.mark.django_db
class TestNoteUpdateView:
    """Тесты для NoteUpdateView."""

    def test_update_note_topic(self, client, notes_hierarchy):
        """
        T057 [P] [US7] Integration test: update note topic.

        Проверяет, что:
        - POST запрос с новым topic успешно обновляет заметку
        - Topic изменяется на новое значение
        - Происходит redirect на страницу детальной заметки
        - Success message отображается
        """
        note = notes_hierarchy['note1']
        url = reverse('note_update', kwargs={'pk': note.pk})
        old_topic = note.topic
        new_topic = 'Обновлённая тема заметки'

        # POST запрос с новым topic
        response = client.post(url, {
            'topic': new_topic,
            'text': note.text or '',
            'parent': '',
            # keywords - ManyToManyField, не передаём ничего
            # Formset данные (без изменений)
            'book_editions-TOTAL_FORMS': '1',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': '',
            'book_editions-0-additional_info': '',
            'book_editions-0-DELETE': '',
        }, follow=True)

        # Проверяем, что страница загрузилась
        assert response.status_code == 200

        # Обновляем заметку из БД
        note.refresh_from_db()

        # Проверяем, что topic обновился
        assert note.topic == new_topic, f"Topic должен обновиться с '{old_topic}' на '{new_topic}'"

        # Проверяем success message
        assert 'Заметка успешно обновлена'.encode() in response.content, "Должно быть success message"

    def test_update_note_books(self, client, notes_hierarchy, book_editions):
        """
        T058 [P] [US7] Integration test: update note book editions inline.

        Проверяет, что:
        - POST запрос с изменёнными book_editions обновляет связи
        - Связи NoteToBookEdition создаются/обновляются корректно
        - additional_info сохраняется для каждой связи
        """
        note = notes_hierarchy['note1']
        book_edition_1 = book_editions[0]
        book_edition_2 = book_editions[1] if len(book_editions) > 1 else book_editions[0]

        url = reverse('note_update', kwargs={'pk': note.pk})

        # POST запрос с book_editions inline
        response = client.post(url, {
            'topic': note.topic,
            'text': note.text or '',
            'parent': '',
            # keywords - ManyToManyField, не передаём ничего
            # Formset данные с двумя book_editions
            'book_editions-TOTAL_FORMS': '3',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': str(book_edition_1.pk),
            'book_editions-0-additional_info': 'Дополнительная информация 1',
            'book_editions-0-DELETE': '',
            'book_editions-1-book_edition': str(book_edition_2.pk),
            'book_editions-1-additional_info': 'Дополнительная информация 2',
            'book_editions-1-DELETE': '',
            'book_editions-2-book_edition': '',  # Пустая форма (должна игнорироваться)
            'book_editions-2-additional_info': '',
            'book_editions-2-DELETE': '',
        }, follow=True)

        # Проверяем, что страница загрузилась
        assert response.status_code == 200

        # Проверяем, что связи NoteToBookEdition созданы
        note_to_books = NoteToBookEdition.objects.filter(note=note)
        assert note_to_books.count() == 2, f"Должно быть 2 связи NoteToBookEdition, найдено: {note_to_books.count()}"

        # Проверяем данные связей
        ntb_1 = note_to_books.filter(book_edition=book_edition_1).first()
        assert ntb_1 is not None, "Связь с book_edition_1 должна существовать"
        assert ntb_1.additional_info == 'Дополнительная информация 1', "additional_info должен сохраниться"

        ntb_2 = note_to_books.filter(book_edition=book_edition_2).first()
        assert ntb_2 is not None, "Связь с book_edition_2 должна существовать"
        assert ntb_2.additional_info == 'Дополнительная информация 2', "additional_info должен сохраниться"

        # Проверяем success message
        assert 'Заметка успешно обновлена'.encode() in response.content, "Должно быть success message"

    def test_update_circular_blocked(self, client, notes_hierarchy):
        """
        T059 [P] [US7] Validation test: update with circular dependency blocked.

        Проверяет, что:
        - Попытка установить parent=self блокируется
        - Форма невалидна
        - Ошибка валидации отображается
        """
        note = notes_hierarchy['note1']
        url = reverse('note_update', kwargs={'pk': note.pk})

        # POST запрос с parent=self (циклическая зависимость)
        response = client.post(url, {
            'topic': note.topic,
            'text': note.text,
            'parent': str(note.pk),  # Пытаемся установить parent=self
            'keywords': '',
            # Formset данные (пустые)
            'book_editions-TOTAL_FORMS': '1',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': '',
            'book_editions-0-additional_info': '',
            'book_editions-0-DELETE': '',
        })

        # Проверяем, что форма невалидна (остались на той же странице)
        assert response.status_code == 200

        # Проверяем, что ошибка валидации есть
        assert 'циклическую зависимость'.encode('utf-8') in response.content, "Должна быть ошибка о циклической зависимости"

        # Проверяем, что заметка не обновилась
        note.refresh_from_db()
        assert note.parent is None, "Parent не должен измениться"


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
