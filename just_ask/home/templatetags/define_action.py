from django import template

register = template.Library()

@register.simple_tag
def define(val):
  return val


@register.simple_tag
def update_variable(value):

  """Allows to update existing variable in template"""
  return value

  