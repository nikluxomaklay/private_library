from operator import itemgetter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.models import Note


def dot_separated_string_to_list(value: str, coerce='default') -> list:
    if coerce == 'default':
        coerce = int
    if coerce:
        return [coerce(v) for v in value.split('.')]
    else:
        return [v for v in value.split('.')]


def list_to_dot_separated_string(value: list) -> str:
    return '.'.join([str(item) for item in value])


def generate_note_number(note: 'Note', query):
    if note.parent_id:
        return _generate_note_number_with_parent(note, query)
    else:
        return _generate_note_number_without_parens(query)


def _generate_note_number_with_parent(note: 'Note', query) -> str:
    parent_index = dot_separated_string_to_list(query.get(pk=note.parent_id).index)
    indexes = [dot_separated_string_to_list(item.index) for item in query.filter(parent_id=note.parent_id)]
    max_minor_index = max(indexes, key=itemgetter(-1), default=[0])
    next_index = parent_index + [max_minor_index[-1] + 1]
    return list_to_dot_separated_string(next_index)

def _generate_note_number_without_parens(query) -> str:
    indexes = [dot_separated_string_to_list(item.index) for item in query.filter(parent_id__isnull=True)]
    max_major_index = max(indexes, key=itemgetter(0), default=[0])
    return list_to_dot_separated_string([max_major_index[0] + 1])
