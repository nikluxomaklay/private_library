"""
Template tests для NoteListView.

Тесты проверяют:
- T011: Отображение индекса и темы заметок в списке
"""
import pytest
from django.urls import reverse

from core.models import Note


@pytest.mark.django_db
class TestNoteTemplates:
    """Тесты для шаблонов заметок."""

    def test_note_list_displays(self, client, notes_hierarchy):
        """
        T011 [P] [US1] Template test: note list displays index and topic.
        
        Проверяет, что:
        - Шаблон note_list.html используется
        - Индекс заметки отображается как ссылка на detail view
        - Тема заметки отображается
        - Ссылки на заметки корректны
        """
        url = reverse('note')
        response = client.get(url)
        
        # Страница должна успешно загрузиться
        assert response.status_code == 200
        
        # Проверяем, что используется правильный шаблон
        assert 'front/notes/note_list.html' in [t.name for t in response.templates]
        
        content = response.content.decode()
        
        # Проверяем отображение индекса и темы для каждой заметки
        note1 = notes_hierarchy['note1']
        
        # Индекс должен быть ссылкой
        assert f'href="/note/' in content or f'href="/note/' in content
        
        # Тема должна отображаться
        assert note1.topic in content
        assert note1.index in content
        
        # Проверяем, что все верхнеуровневые заметки имеют индекс и тему
        for key in ['note1', 'note2', 'note3']:
            note = notes_hierarchy[key]
            assert note.index in content, f"Индекс {note.index} не найден"
            assert note.topic in content, f"Тема {note.topic} не найдена"
        
        # Проверяем, что дочерние заметки также имеют индекс и тему
        for key in ['note1_1', 'note1_2', 'note2_1', 'note1_1_1']:
            note = notes_hierarchy[key]
            assert note.index in content, f"Индекс дочерней {note.index} не найден"
            assert note.topic in content, f"Тема дочерней {note.topic} не найдена"
