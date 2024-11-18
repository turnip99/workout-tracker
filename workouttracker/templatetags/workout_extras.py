from django import template

register = template.Library()

@register.filter
def capitalise_and_underscore_to_space(value):
    return value.replace("_"," ").capitalize()