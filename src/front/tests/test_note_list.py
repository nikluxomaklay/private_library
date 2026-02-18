"""
Integration tests для NoteListView.

Тесты проверяют:
- T009: Отображение иерархии заметок с отступами
- T010: Пагинация применяется только к верхнеуровневым заметкам
"""
import pytest
from django.urls import reverse

from core.models import Note


@pytest.mark.django_db
class TestNoteListView:
    """Тесты для NoteListView."""

    def test_note_list_hierarchy(self, client, notes_hierarchy):
        """
        T009 [P] [US1] Integration test: note list page renders with hierarchy.
        
        Проверяет, что:
        - Страница списка заметок успешно загружается
        - Верхнеуровневые заметки отображаются
        - Дочерние заметки отображаются с отступами (padding-left)
        - Иерархическая структура сохраняется
        """
        url = reverse('note')
        response = client.get(url)
        
        # Страница должна успешно загрузиться
        assert response.status_code == 200
        
        # Проверяем, что верхнеуровневые заметки отображаются
        note1 = notes_hierarchy['note1']
        note2 = notes_hierarchy['note2']
        note3 = notes_hierarchy['note3']
        
        # Проверяем наличие индексов и тем верхнеуровневых заметок
        assertContains(response, note1.index)
        assertContains(response, note1.topic)
        assertContains(response, note2.index)
        assertContains(response, note2.topic)
        assertContains(response, note3.index)
        assertContains(response, note3.topic)
        
        # Проверяем, что дочерние заметки также отображаются
        note1_1 = notes_hierarchy['note1_1']
        note1_2 = notes_hierarchy['note1_2']
        note2_1 = notes_hierarchy['note2_1']
        note1_1_1 = notes_hierarchy['note1_1_1']
        
        assertContains(response, note1_1.index)
        assertContains(response, note1_1.topic)
        assertContains(response, note1_2.index)
        assertContains(response, note1_2.topic)
        assertContains(response, note2_1.index)
        assertContains(response, note2_1.topic)
        assertContains(response, note1_1_1.index)
        assertContains(response, note1_1_1.topic)
        
        # Проверяем, что дочерние заметки имеют отступы (margin-left в стилях)
        content = response.content.decode()
        # Дочерние заметки должны иметь margin-left для отступа
        assert 'margin-left' in content, "Дочерние заметки должны иметь отступы (margin-left)"

    def test_note_list_pagination(self, client, many_top_level_notes):
        """
        T010 [P] [US1] Integration test: pagination applies to top-level notes only.
        
        Проверяет, что:
        - Пагинация применяется только к верхнеуровневым заметкам
        - При размере страницы 10, на первой странице 10 верхнеуровневых заметок
        - Дочерние заметки отображаются с родителями и не влияют на пагинацию
        """
        # Создадим дочерние заметки для некоторых верхнеуровневых
        for i, note in enumerate(many_top_level_notes[:5]):
            Note.objects.create(
                index=f'{note.index}.1',
                topic=f'Дочерняя заметка {note.index}.1',
                parent=note
            )
        
        url = reverse('note')
        
        # Запрос с размером страницы 10
        response = client.get(url, {'page_size': '10'})
        assert response.status_code == 200
        
        content = response.content.decode()
        
        # Проверяем, что пагинация присутствует
        assert 'pagination' in content or 'page-link' in content
        
        # Проверяем, что на первой странице 10 верхнеуровневых заметок + дочерние
        # Индексы сортируются как строки, поэтому '1', '10', '11', ... '18', '19', '2'
        # Считаем только верхнеуровневые заметки (без отступа margin-left)
        # Верхнеуровневые заметки имеют style="" или не имеют style с margin-left
        import re
        # Находим все badge с индексами верхнеуровневых заметок (без margin-left в родительском li)
        top_level_pattern = r'<li class="note-item[^"]*"[^>]*style="">.*?<span class="badge bg-secondary">(\d+)</span>'
        top_level_matches = re.findall(top_level_pattern, content, re.DOTALL)
        
        # Должно быть 10 верхнеуровневых заметок на странице
        assert len(top_level_matches) == 10, f"На первой странице должно быть 10 верхнеуровневых заметок, найдено: {len(top_level_matches)}"
        
        # Проверяем, что дочерние заметки также отображаются (с margin-left)
        # На первой странице только заметка '1' имеет дочернюю заметку, потому что
        # другие заметки с дочерними ('10', '11', '12', '13', '14') не имеют созданных дочерних
        # (мы создали дочерние только для первых 5 заметок: '1', '2', '3', '4', '5')
        # Но из-за сортировки строк, на первой странице только '1' из этих заметок
        child_pattern = r'<li class="note-item[^"]*"[^>]*style="margin-left:.*?<span class="badge bg-secondary">([\d.]+)</span>'
        child_matches = re.findall(child_pattern, content, re.DOTALL)
        # На первой странице должна быть 1 дочерняя заметка (у заметки '1')
        assert len(child_matches) >= 1, f"Должна быть хотя бы 1 дочерняя заметка, найдено: {len(child_matches)}"
        
        # Перейдем на вторую страницу
        response_page2 = client.get(url, {'page': '2', 'page_size': '10'})
        assert response_page2.status_code == 200
        
        content_page2 = response_page2.content.decode()
        
        # На второй странице также должно быть 10 верхнеуровневых заметок
        top_level_matches_page2 = re.findall(top_level_pattern, content_page2, re.DOTALL)
        assert len(top_level_matches_page2) == 10, f"На второй странице должно быть 10 верхнеуровневых заметок"
        
        # Третья страница должна содержать оставшиеся 5 верхнеуровневых заметок
        response_page3 = client.get(url, {'page': '3', 'page_size': '10'})
        assert response_page3.status_code == 200
        
        content_page3 = response_page3.content.decode()
        top_level_matches_page3 = re.findall(top_level_pattern, content_page3, re.DOTALL)
        assert len(top_level_matches_page3) == 5, f"На третьей странице должно быть 5 верхнеуровневых заметок"


def assertContains(response, text):
    """Вспомогательная функция для проверки наличия текста в ответе."""
    content = response.content.decode()
    assert text in content, f"Текст '{text}' не найден в ответе"
