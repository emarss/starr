from django import template
register = template.Library()

@register.filter
def get_value(dictionary, key):
	"""Gives the value of a dictionary"""
	return dictionary[key]
