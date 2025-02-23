from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Retourne la multiplication de deux nombres"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
