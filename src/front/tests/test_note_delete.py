"""
Integration tests для удаления заметок (NoteDeleteView).

Тесты проверяют:
- T069: Удаление заметки без дочерних элементов
- T070: Блокировка удаления заметки с дочерними элементами
"""
import pytest
from django.urls import reverse

from core.models import Note


@pytest.mark.django_db
class TestNoteDeleteView:
    """Тесты для NoteDeleteView."""

    def test_delete_note_without_children(self, client, notes_hierarchy):
        """
        T069 [P] [US8] Integration test: delete note without children.

        Проверяет, что:
        - POST запрос на удаление заметки без детей успешно удаляет заметку
        - Происходит redirect на страницу списка заметок
        - Success message отображается
        - Заметка действительно удалена из БД
        """
        # Создаем заметку без детей (используем note3 из fixtures)
        note = notes_hierarchy['note3']
        note_pk = note.pk
        url = reverse('note_delete', kwargs={'pk': note_pk})

        # Проверяем, что заметка существует до удаления
        assert Note.objects.filter(pk=note_pk).exists(), "Заметка должна существовать до удаления"

        # POST запрос на удаление
        response = client.post(url, follow=True)

        # Проверяем, что redirect произошел на список заметок
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse('note'), "Должен быть redirect на note"

        # Проверяем, что заметка удалена из БД
        assert not Note.objects.filter(pk=note_pk).exists(), "Заметка должна быть удалена из БД"

        # Проверяем success message
        assert 'Заметка успешно удалена'.encode('utf-8') in response.content, "Должно быть success message"

    def test_delete_note_with_children_blocked(self, client, notes_hierarchy):
        """
        T070 [P] [US8] Validation test: delete note with children blocked.

        Проверяет, что:
        - Попытка удалить заметку с дочерними блокируется
        - Заметка НЕ удаляется из БД
        - Error message отображается
        - Происходит redirect на страницу детальной заметки
        """
        # Используем note1, у которой есть дети (note1_1, note1_2)
        note = notes_hierarchy['note1']
        note_pk = note.pk
        url = reverse('note_delete', kwargs={'pk': note_pk})

        # Проверяем, что у заметки есть дети
        assert note.children.exists(), "У заметки должны быть дети для этого теста"
        children_count_before = note.children.count()

        # POST запрос на удаление
        response = client.post(url, follow=True)

        # Проверяем, что redirect произошел на детальную страницу заметки
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse('note_detail', kwargs={'pk': note_pk}), \
            "Должен быть redirect на note_detail"

        # Проверяем, что заметка НЕ удалена из БД
        assert Note.objects.filter(pk=note_pk).exists(), "Заметка должна остаться в БД"

        # Проверяем, что дети остались на месте
        note.refresh_from_db()
        assert note.children.count() == children_count_before, "Дети должны остаться на месте"

        # Проверяем error message
        assert 'Нельзя удалить заметку с дочерними заметками'.encode('utf-8') in response.content, \
            "Должно быть error message о невозможности удаления с детьми"
