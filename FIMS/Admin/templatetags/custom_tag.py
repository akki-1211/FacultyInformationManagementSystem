from django import template
from django.template.defaultfilters import stringfilter

path = ""
register = template.Library()
@register.filter(name='split')
@stringfilter
def split(value,key):
    s = value.split(key)
    print(s)
    return s

@register.simple_tag
def setvar(val=""):
    return val

@register.simple_tag
@stringfilter
def addstr(val):
    global path
    if path == "":
        path = val
        return val
    path += '/'+val
    print(path)
    return path

@register.simple_tag
def reassign():
    global path
    path = ""
    return ""