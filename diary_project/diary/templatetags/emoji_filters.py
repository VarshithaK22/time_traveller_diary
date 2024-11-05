from django import template

register = template.Library()


@register.filter
def get_emoji(value):
    # Split the string and return the last part (emoji)
    return value.split()[-1]
