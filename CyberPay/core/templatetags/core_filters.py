from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter(name='currency')
def currency_filter(value, arg=-1):
    if value < 0:
        return "(${})".format(intcomma(floatformat(value * -1, arg)))
    else:
        return "${}".format(intcomma(floatformat(value, arg)))
