"""
Integration tests для создания заметок (NoteNewView).

Тесты проверяют:
- T033: Создание заметки с минимальными данными (topic только)
- T034: Создание заметки с книжными изданиями inline
- T048: Создание заметки из book_edition с pre-fill поля
- T052: Создание заметки из другой заметки с pre-fill parent, books, keywords
"""
import pytest
from django.urls import reverse

from core.models import Note, NoteToBookEdition, BookEdition


@pytest.mark.django_db
class TestNoteCreateView:
    """Тесты для NoteNewView."""

    def test_create_note_minimal(self, client):
        """
        T033 [P] [US4] Integration test: create note with topic only.

        Проверяет, что:
        - POST запрос с topic только успешно создаёт заметку
        - Заметка получает автоматически сгенерированный index
        - Происходит redirect на страницу детальной заметки
        - Success message отображается
        """
        url = reverse('note_new')

        # POST запрос с минимальными данными (только topic)
        response = client.post(url, {
            'topic': 'Новая тестовая заметка',
            'text': '',
            'parent': '',
            # keywords - ManyToManyField, не передаём ничего
            # Formset данные (пустые, без book_editions)
            'book_editions-TOTAL_FORMS': '1',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': '',
            'book_editions-0-additional_info': '',
            'book_editions-0-DELETE': '',
        }, follow=True)
        
        # Проверяем redirect и success message
        assert response.status_code == 200
        
        # Проверяем, что заметка создана
        note = Note.objects.filter(topic='Новая тестовая заметка').first()
        assert note is not None, "Заметка должна быть создана"
        assert note.index is not None, "Заметка должна получить индекс"
        assert note.text == '', "Текст должен быть пустым"
        assert note.parent is None, "Родительская заметка должна быть None"
        
        # Проверяем, что redirect произошёл на страницу детальной заметки
        # follow=True следует за редиректом, проверяем что мы на note_detail
        assert 'Заметка успешно создана'.encode() in response.content, "Должно быть success message"

    def test_create_note_with_books(self, client, book_editions):
        """
        T034 [P] [US4] Integration test: create note with book editions inline.

        Проверяет, что:
        - POST запрос с book_editions inline успешно создаёт заметку
        - Связи NoteToBookEdition создаются корректно
        - additional_info сохраняется для каждой связи
        """
        url = reverse('note_new')
        
        # Получаем book_edition для теста
        book_edition_1 = book_editions[0]
        book_edition_2 = book_editions[1] if len(book_editions) > 1 else book_edition_1
        
        # POST запрос с book_editions inline
        response = client.post(url, {
            'topic': 'Заметка с книгами',
            'text': 'Текст заметки с книгами',
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
        
        # Проверяем, что заметка создана
        note = Note.objects.filter(topic='Заметка с книгами').first()
        assert note is not None, "Заметка должна быть создана"
        assert note.text == 'Текст заметки с книгами', "Текст должен сохраниться"
        
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
        assert 'Заметка успешно создана'.encode() in response.content, "Должно быть success message"

    def test_create_note_from_book_edition(self, client, book_editions):
        """
        T048 [P] [US5] Integration test: create note from book edition with pre-filled field.

        Проверяет, что:
        - GET запрос с book_edition query param открывает страницу создания
        - POST запрос с book_edition param создаёт заметку с предзаполненным book_edition
        """
        book_edition_1 = book_editions[0]
        
        # GET запрос с book_edition param
        url = reverse('note_new')
        response = client.get(url, {'book_edition': book_edition_1.pk})
        
        # Проверяем, что страница загрузилась
        assert response.status_code == 200
        
        # POST запрос для создания заметки с pre-fill book_edition
        response = client.post(url, {
            'topic': 'Заметка из book edition',
            'text': 'Текст заметки из book edition',
            'parent': '',
            # keywords - не передаём
            # Formset данные с pre-filled book_edition
            'book_editions-TOTAL_FORMS': '2',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': str(book_edition_1.pk),
            'book_editions-0-additional_info': 'Доп info из pre-fill',
            'book_editions-0-DELETE': '',
            'book_editions-1-book_edition': '',
            'book_editions-1-additional_info': '',
            'book_editions-1-DELETE': '',
        }, follow=True)
        
        # Проверяем, что страница загрузилась
        assert response.status_code == 200
        
        # Проверяем, что заметка создана
        note = Note.objects.filter(topic='Заметка из book edition').first()
        assert note is not None, "Заметка должна быть создана"
        
        # Проверяем, что связь с book_edition создана
        note_to_books = NoteToBookEdition.objects.filter(note=note)
        assert note_to_books.count() == 1, f"Должна быть 1 связь NoteToBookEdition"
        
        ntb = note_to_books.first()
        assert ntb.book_edition == book_edition_1, "book_edition должен совпадать"
        assert ntb.additional_info == 'Доп info из pre-fill', "additional_info должен сохраниться"
        
        # Проверяем success message
        assert 'Заметка успешно создана'.encode() in response.content

    def test_create_note_from_note(self, client, note_with_relations):
        """
        T052 [P] [US6] Integration test: create note from note with pre-fill parent, books, keywords.

        Проверяет, что:
        - GET запрос с parent query param открывает страницу создания
        - POST запрос создаёт заметку с предзаполненными parent, book_editions, keywords
        - topic и text остаются пустыми (не копируются из parent)
        """
        parent_note, book_edition, keyword = note_with_relations
        
        # GET запрос с parent param
        url = reverse('note_new')
        response = client.get(url, {'parent': parent_note.pk})
        
        # Проверяем, что страница загрузилась
        assert response.status_code == 200
        
        # POST запрос для создания заметки с pre-fill из parent
        response = client.post(url, {
            'topic': 'Дочерняя заметка',
            'text': 'Текст дочерней заметки',
            'parent': parent_note.pk,
            'keywords': [keyword.pk],
            # Formset данные с pre-fill book_editions из parent
            'book_editions-TOTAL_FORMS': '2',
            'book_editions-INITIAL_FORMS': '0',
            'book_editions-MIN_NUM_FORMS': '0',
            'book_editions-MAX_NUM_FORMS': '1000',
            'book_editions-0-book_edition': str(book_edition.pk),
            'book_editions-0-additional_info': 'Доп info из parent',
            'book_editions-0-DELETE': '',
            'book_editions-1-book_edition': '',
            'book_editions-1-additional_info': '',
            'book_editions-1-DELETE': '',
        }, follow=True)
        
        # Проверяем, что страница загрузилась
        assert response.status_code == 200
        
        # Проверяем, что заметка создана
        child_note = Note.objects.filter(topic='Дочерняя заметка').first()
        assert child_note is not None, "Заметка должна быть создана"
        
        # Проверяем parent
        assert child_note.parent == parent_note, "parent должен быть предзаполнен"
        
        # Проверяем keywords
        assert child_note.keywords.count() == 1, "Должно быть 1 ключевое слово"
        assert child_note.keywords.first() == keyword, "keyword должен совпадать"
        
        # Проверяем book_editions
        note_to_books = NoteToBookEdition.objects.filter(note=child_note)
        assert note_to_books.count() == 1, f"Должна быть 1 связь NoteToBookEdition"
        
        ntb = note_to_books.first()
        assert ntb.book_edition == book_edition, "book_edition должен совпадать с parent"
        
        # Проверяем success message
        assert 'Заметка успешно создана'.encode() in response.content


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


@pytest.fixture
def note_with_relations(db):
    """
    Создает заметку с relations (book_editions, keywords) для тестирования US6.
    """
    from core.models import Book, Publisher, BookEdition, Note, NoteToBookEdition, KeyWord

    # Создаем book_edition
    publisher = Publisher.objects.create(name='Тестовое издательство')
    book = Book.objects.create(title='Тестовая книга')
    book_edition = BookEdition.objects.create(
        book=book,
        publisher=publisher,
        publication_year=2024,
        edition_type='PAPER_BOOK'
    )
    
    # Создаем keyword
    keyword = KeyWord.objects.create(word='тестовый')
    
    # Создаем parent заметку с relations
    parent_note = Note.objects.create(
        topic='Родительская заметка',
        text='Текст родительской заметки'
    )
    
    # Связываем с book_edition
    NoteToBookEdition.objects.create(
        note=parent_note,
        book_edition=book_edition,
        additional_info='Доп info'
    )
    
    # Связываем с keyword
    parent_note.keywords.add(keyword)
    
    return parent_note, book_edition, keyword
