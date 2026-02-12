from django import template

register = template.Library()


@register.simple_tag
def edition_type_icon(edition_type):
    """
    Returns the Unicode icon for the given edition type.
    
    Args:
        edition_type (str): The edition type code (PAPER_BOOK, EBOOK, etc.)
        
    Returns:
        str: The corresponding Unicode icon
    """
    icon_map = {
        'PAPER_BOOK': '📖',
        'EBOOK': '📄',
        'AUDIOBOOK': '🎙️',
        'WEBPAGE': '🌐',
    }
    return icon_map.get(edition_type, '')


@register.simple_tag
def edition_type_display(edition_type):
    """
    Returns the display name for the given edition type.
    
    Args:
        edition_type (str): The edition type code (PAPER_BOOK, EBOOK, etc.)
        
    Returns:
        str: The display name for the edition type
    """
    display_map = {
        'PAPER_BOOK': 'Paper Book',
        'EBOOK': 'E-book',
        'AUDIOBOOK': 'Audiobook',
        'WEBPAGE': 'Web Page',
    }
    return display_map.get(edition_type, edition_type)