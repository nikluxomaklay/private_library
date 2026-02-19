"""
Integration tests для NoteDetailView.

Тесты проверяют:
- T019: Отображение всех полей заметки на детальной странице
- T020: Отображение связанных книжных изданий с additional_info
"""
import pytest
from django.urls import reverse

from core.models import Note, KeyWord, NoteToBookEdition, Book, BookEdition, Publisher


def assertContains(response, text):
    """Вспомогательная функция для проверки наличия текста в ответе."""
    content = response.content.decode()
    assert text in content, f"Текст '{text}' не найден в ответе"


def assertNotContains(response, text):
    """Вспомогательная функция для проверки отсутствия текста в ответе."""
    content = response.content.decode()
    assert text not in content, f"Текст '{text}' найден в ответе, хотя не должен быть"


@pytest.mark.django_db
class TestNoteDetailView:
    """Тесты для NoteDetailView."""

    def test_note_detail_displays_all(self, client):
        """
        T019 [P] [US2] Integration test: note detail page displays all fields.

        Проверяет, что:
        - Страница детальной заметки успешно загружается
        - Отображаются все поля: topic, text, parent, keywords
        - Parent отображается ссылкой на родительскую заметку
        - Keywords отображаются списком
        """
        # Создадим родительскую заметку
        parent_note = Note.objects.create(
            index='1',
            topic='Родительская заметка',
            text='Текст родительской заметки'
        )

        # Создадим ключевые слова
        keyword1 = KeyWord.objects.create(word='ключ1')
        keyword2 = KeyWord.objects.create(word='ключ2')

        # Создадим заметку со всеми полями
        note = Note.objects.create(
            index='1.1',
            topic='Тема дочерней заметки',
            text='Текст дочерней заметки',
            parent=parent_note
        )
        note.keywords.add(keyword1, keyword2)

        # Запросим детальную страницу
        url = reverse('note_detail', kwargs={'pk': note.pk})
        response = client.get(url)

        # Страница должна успешно загрузиться
        assert response.status_code == 200

        # Проверяем отображение всех полей
        # Topic (заголовок)
        assertContains(response, note.topic)

        # Text
        assertContains(response, note.text)

        # Index
        assertContains(response, note.index)

        # Parent (ссылка на родительскую заметку)
        assertContains(response, parent_note.topic)
        # Проверяем, что parent отображается ссылкой
        content = response.content.decode()
        assert f'href="{reverse("note_detail", kwargs={"pk": parent_note.pk})}"' in content

        # Keywords (список)
        assertContains(response, keyword1.word)
        assertContains(response, keyword2.word)

    def test_note_detail_book_editions(self, client):
        """
        T020 [P] [US2] Integration test: note detail shows related book editions with info.

        Проверяет, что:
        - Страница детальной заметки отображает связанные книжные издания
        - additional_info отображается для каждого NoteToBookEdition
        """
        # Создадим книгу и издание
        publisher = Publisher.objects.create(name='Издательство')
        book = Book.objects.create(title='Название книги')
        book_edition = BookEdition.objects.create(
            book=book,
            publisher=publisher,
            publication_year=2024,
            edition_type='PAPER_BOOK'
        )

        # Создадим заметку
        note = Note.objects.create(
            index='1',
            topic='Тема заметки',
            text='Текст заметки'
        )

        # Создадим связь NoteToBookEdition с additional_info
        note_to_book = NoteToBookEdition.objects.create(
            note=note,
            book_edition=book_edition,
            additional_info='Дополнительная информация о связи'
        )

        # Запросим детальную страницу
        url = reverse('note_detail', kwargs={'pk': note.pk})
        response = client.get(url)

        # Страница должна успешно загрузиться
        assert response.status_code == 200

        # Проверяем отображение book_edition
        assertContains(response, book.title)
        assertContains(response, str(publisher))
        assertContains(response, str(book_edition.publication_year))

        # Проверяем отображение additional_info
        assertContains(response, note_to_book.additional_info)
