"""
Fixtures для тестирования views и templates заметок.
"""
import os
import sys
from pathlib import Path

import pytest
from django.conf import settings

# Настраиваем Django settings
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'private_library.settings')

import django
django.setup()

from django.urls import reverse

from core.models import Note, KeyWord


@pytest.fixture
def notes_hierarchy(db):
    """
    Создает иерархию заметок для тестирования.
    
    Структура:
    - Note 1 (parent=None)
      - Note 1.1 (parent=Note 1)
        - Note 1.1.1 (parent=Note 1.1)
      - Note 1.2 (parent=Note 1)
    - Note 2 (parent=None)
      - Note 2.1 (parent=Note 2)
    - Note 3 (parent=None)
    """
    # Верхнеуровневые заметки
    note1 = Note.objects.create(
        index='1',
        topic='Тема заметки 1',
        text='Текст заметки 1'
    )
    note2 = Note.objects.create(
        index='2',
        topic='Тема заметки 2',
        text='Текст заметки 2'
    )
    note3 = Note.objects.create(
        index='3',
        topic='Тема заметки 3',
        text='Текст заметки 3'
    )
    
    # Дочерние заметки первого уровня
    note1_1 = Note.objects.create(
        index='1.1',
        topic='Тема заметки 1.1',
        text='Текст заметки 1.1',
        parent=note1
    )
    note1_2 = Note.objects.create(
        index='1.2',
        topic='Тема заметки 1.2',
        text='Текст заметки 1.2',
        parent=note1
    )
    note2_1 = Note.objects.create(
        index='2.1',
        topic='Тема заметки 2.1',
        text='Текст заметки 2.1',
        parent=note2
    )
    
    # Дочерние заметки второго уровня
    note1_1_1 = Note.objects.create(
        index='1.1.1',
        topic='Тема заметки 1.1.1',
        text='Текст заметки 1.1.1',
        parent=note1_1
    )
    
    return {
        'note1': note1,
        'note2': note2,
        'note3': note3,
        'note1_1': note1_1,
        'note1_2': note1_2,
        'note2_1': note2_1,
        'note1_1_1': note1_1_1,
    }


@pytest.fixture
def many_top_level_notes(db):
    """
    Создает много верхнеуровневых заметок для тестирования пагинации.
    """
    notes = []
    for i in range(1, 26):  # 25 заметок
        note = Note.objects.create(
            index=str(i),
            topic=f'Тема заметки {i}',
            text=f'Текст заметки {i}'
        )
        notes.append(note)
    return notes


@pytest.fixture
def client_with_notes(client, notes_hierarchy):
    """
    Клиент с созданной иерархией заметок.
    """
    return client


@pytest.fixture
def keywords(db):
    """
    Создает ключевые слова для тестирования.
    """
    kw1 = KeyWord.objects.create(word='ключ1')
    kw2 = KeyWord.objects.create(word='ключ2')
    return {'kw1': kw1, 'kw2': kw2}
