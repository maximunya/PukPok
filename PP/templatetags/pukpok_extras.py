from django import template


register = template.Library()


@register.filter
def filter_posts(value):
	result = value.filter(is_published=True).count()
	return result
