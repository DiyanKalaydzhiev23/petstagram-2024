from django import template

register = template.Library()

@register.filter
def placeholder(value, text_to_be_placed):
    value.field.widget.attrs['placeholder'] = text_to_be_placed
    return value