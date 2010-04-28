from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def limit(value, max):
    if len(value) > max:
        return "%s..." % value[:max]
    else:
        return value