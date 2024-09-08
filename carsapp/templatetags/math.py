from django import template

register = template.Library()


@register.filter(name="sub")
def subtraction(value, arg):
    return int(value) - int(arg)


@register.filter(name="min")
def find_min(value, arg):
    return min(int(value), int(arg))
