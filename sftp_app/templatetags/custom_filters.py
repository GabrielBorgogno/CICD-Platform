# Inside custom_filters.py
from django import template
import os

register = template.Library()

@register.filter(name='file_extension')
def file_extension(value):
    return os.path.splitext(value)[1][1:].lower()  # Get the lowercase file extension without the dot
