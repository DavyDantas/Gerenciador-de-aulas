from django import template
from django.contrib.auth.models import Group
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary[key] 

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def re_absent(value):
    data = str(value)
    return re.sub(r'[\[\]"\']', '', data)