from dataclasses import dataclass
from operator import itemgetter
from typing import TYPE_CHECKING

from django.db import transaction

if TYPE_CHECKING:
    from core.models import Note


def dot_separated_string_to_list(value: str, coerce='default') -> list:
    if coerce == 'default':
        coerce = int
    if coerce:
        return [coerce(v) for v in value.split('.')]
    else:
        return [v for v in value.split('.')]


def list_to_dot_separated_string(value: list) -> str:
    return '.'.join([str(item) for item in value])


def update_children_indexes(
    note: 'Note',
    query = None,
    first_iteration: bool = True,
    exclude_ids: list[int] | None = None,
):
    from core.models import Note

    def _update_children(_note, _query, _exclude_ids):
        if _exclude_ids is None:
            _exclude_ids = list(_note.children.values_list('id', flat=True))

        for_update = []
        for child in _note.children.order_by('id'):
            child.index = generate_note_index(_note.id, _query, exclude_ids=_exclude_ids)
            for_update.append(child)
            _exclude_ids.remove(child.id)

        Note.objects.bulk_update(for_update, ['index'])

        for child in for_update:
            update_children_indexes(child, query=_query, first_iteration=False)

    if not query:
        query = Note.objects.select_for_update().filter(root=note.root)

    if first_iteration:
        with transaction.atomic():
            _update_children(note, query, exclude_ids)
    else:
        _update_children(note, query, exclude_ids)


def generate_note_index(parent_id: int = None, query = None, exclude_ids: list[int] | None = None) -> str:
    if query is None:
        from core.models import Note
        query = Note.objects.select_for_update().all()

    with transaction.atomic():
        if parent_id:
            return _generate_note_index_with_parent(parent_id, query, exclude_ids)
        else:
            return _generate_note_index_without_parens(query, exclude_ids)


def _generate_note_index_with_parent(parent_id: int, query, exclude_ids: list[int] | None = None) -> str:
    parent_index = dot_separated_string_to_list(query.get(pk=parent_id).index)
    child_query = query.filter(parent_id=parent_id)
    if exclude_ids:
        child_query = child_query.exclude(id__in=exclude_ids)
    indexes = [dot_separated_string_to_list(item.index)[:len(parent_index) + 1] for item in child_query]
    max_minor_index = max(indexes, key=itemgetter(-1), default=[0])[-1]
    next_index = parent_index + [max_minor_index + 1]
    return list_to_dot_separated_string(next_index)

def _generate_note_index_without_parens(query, exclude_ids: list[int] | None = None) -> str:
    if exclude_ids:
        query = query.exclude(id__in=exclude_ids)
    indexes = [dot_separated_string_to_list(item.index) for item in query.filter(parent_id__isnull=True)]
    max_major_index = max(indexes, key=itemgetter(0), default=[0])[0]
    return list_to_dot_separated_string([max_major_index + 1])


@dataclass
class NoteIndexGapSegment:
    segment_start: int
    segment_end: int
    gap: int

    def __init__(self, segment_start: int, segment_length: int, gap: int):
        self.segment_start = segment_start
        self.segment_end = segment_start + segment_length - 1
        self.gap = gap

    def __contains__(self, item):
        return self.segment_start <= item <= self.segment_end


@transaction.atomic
def compress_note_indexes():
    from core.models import Note
    query = Note.objects.select_for_update()
    if not query.exists():
        return

    major_indexes = [
        dot_separated_string_to_list(item.index)[0]
        for item in query.filter(parent_id__isnull=True)
    ]
    max_major_index = max(major_indexes)
    gap_segments = []
    segment_length = 0
    segment_start = 0
    gap = 0
    for major_index in range(1, max_major_index):
        if major_index in major_indexes:
            if segment_length != 0:
                gap_segments.append(
                    NoteIndexGapSegment(segment_start, segment_length, gap),
                )
                segment_length = 0
        else:
            if segment_length == 0:
                segment_start = major_index
            segment_length += 1
            gap += 1

    if segment_length != 0:
        gap_segments.append(
            NoteIndexGapSegment(
                segment_start, max_major_index - segment_start + 1,
                gap,
            ),
        )

    for_update = []
    for note in query:
        for segment in gap_segments:
            separated_index = dot_separated_string_to_list(note.index)
            if separated_index[0] in segment:
                separated_index[0] -= segment.gap
                note.index = list_to_dot_separated_string(separated_index)
                for_update.append(note)
                break

    if for_update:
        query.bulk_update(for_update, ['index'])

    for note in for_update:
        update_children_indexes(note)
