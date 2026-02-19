"""
Integration tests для отображения заметок на странице книжного издания (BookEditionDetailView).

Тесты проверяют:
- T027: Заметки отображаются на странице book_edition
- T028: Иерархия заметок отображается корректно
"""
import pytest
from django.urls import reverse

from core.models import Note, NoteToBookEdition, BookEdition


@pytest.mark.django_db
class TestBookEditionDetailNotes:
    """Тесты для отображения заметок на странице book_edition (US3)."""

    def test_book_edition_shows_notes(self, client, book_edition_with_notes):
        """
        T027 [P] [US3] Integration test: book edition detail shows related notes.

        Проверяет, что:
        - Страница book_edition отображает связанные заметки
        - Индексы и темы заметок видны на странице
        """
        book_edition, notes = book_edition_with_notes
        url = reverse('book_edition_detail', kwargs={'pk': book_edition.pk})

        response = client.get(url)

        # Проверяем, что страница загрузилась
        assert response.status_code == 200

        # Проверяем, что заметки отображаются
        for note in notes:
            # Индекс заметки должен быть на странице
            assert note.index.encode() in response.content, \
                f"Индекс заметки {note.index} должен отображаться"
            # Тема заметки должна быть на странице
            assert note.topic.encode() in response.content, \
                f"Тема заметки '{note.topic}' должна отображаться"

        # Проверяем, что блок "Связанные заметки" присутствует
        content = response.content.decode()
        has_notes_block = 'Связанные заметки' in content or 'Related notes' in content
        assert has_notes_block, "Должен быть блок 'Связанные заметки'"

    def test_book_edition_notes_hierarchy(self, client, book_edition_with_hierarchical_notes):
        """
        T028 [P] [US3] Integration test: related notes display hierarchy.

        Проверяет, что:
        - Дочерние заметки отображаются с отступами
        - Иерархическая структура видна через CSS классы или стили
        """
        book_edition, parent_note, child_notes = book_edition_with_hierarchical_notes
        url = reverse('book_edition_detail', kwargs={'pk': book_edition.pk})

        response = client.get(url)

        # Проверяем, что страница загрузилась
        assert response.status_code == 200

        # Проверяем, что родительская заметка отображается
        assert parent_note.index.encode() in response.content, \
            f"Индекс родительской заметки {parent_note.index} должен отображаться"

        # Проверяем, что дочерние заметки отображаются
        for child_note in child_notes:
            assert child_note.index.encode() in response.content, \
                f"Индекс дочерней заметки {child_note.index} должен отображаться"

        # Проверяем, что есть индикация иерархии (отступы через margin-left или note-children класс)
        content = response.content.decode()
        # Ищем признаки иерархического отображения
        has_hierarchy = (
            'margin-left' in content or
            'note-children' in content or
            'has-children' in content
        )
        assert has_hierarchy, "Должна быть индикация иерархии (отступы или классы)"


@pytest.fixture
def book_edition_with_notes(db):
    """
    Создает book_edition с несколькими заметками для тестирования.
    """
    from core.models import Book, Publisher, BookEdition, Note, NoteToBookEdition

    # Создаем book_edition
    publisher = Publisher.objects.create(name='Тестовое издательство')
    book = Book.objects.create(title='Тестовая книга')
    book_edition = BookEdition.objects.create(
        book=book,
        publisher=publisher,
        publication_year=2024,
        edition_type='PAPER_BOOK'
    )

    # Создаем заметки, связанные с book_edition
    notes = []
    for i in range(3):
        note = Note.objects.create(
            topic=f'Заметка {i+1}',
            text=f'Текст заметки {i+1}'
        )
        NoteToBookEdition.objects.create(
            note=note,
            book_edition=book_edition,
            additional_info=f'Доп info {i+1}'
        )
        notes.append(note)

    return book_edition, notes


@pytest.fixture
def book_edition_with_hierarchical_notes(db):
    """
    Создает book_edition с иерархией заметок (родитель + дети) для тестирования.
    """
    from core.models import Book, Publisher, BookEdition, Note, NoteToBookEdition

    # Создаем book_edition
    publisher = Publisher.objects.create(name='Тестовое издательство')
    book = Book.objects.create(title='Тестовая книга')
    book_edition = BookEdition.objects.create(
        book=book,
        publisher=publisher,
        publication_year=2024,
        edition_type='PAPER_BOOK'
    )

    # Создаем родительскую заметку
    parent_note = Note.objects.create(
        topic='Родительская заметка',
        text='Текст родительской заметки'
    )
    NoteToBookEdition.objects.create(
        note=parent_note,
        book_edition=book_edition,
        additional_info='Доп info родителя'
    )

    # Создаем дочерние заметки
    child_notes = []
    for i in range(2):
        child_note = Note.objects.create(
            topic=f'Дочерняя заметка {i+1}',
            text=f'Текст дочерней заметки {i+1}',
            parent=parent_note
        )
        NoteToBookEdition.objects.create(
            note=child_note,
            book_edition=book_edition,
            additional_info=f'Доп info ребенка {i+1}'
        )
        child_notes.append(child_note)

    return book_edition, parent_note, child_notes
