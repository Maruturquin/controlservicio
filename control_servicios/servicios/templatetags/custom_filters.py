from django import template
from datetime import date

register = template.Library()

@register.filter
def days_until(value):
    if value:
        return (value - date.today()).days
    return 0
