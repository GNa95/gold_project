from django import template

register = template.Library()

@register.filter

def sub_filter(value, arg):
    return value - arg