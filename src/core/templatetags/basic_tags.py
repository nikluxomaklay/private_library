from django import template

register = template.Library()


@register.filter(is_safe=False)
def multiply(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ""
