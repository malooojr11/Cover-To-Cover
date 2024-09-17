from django import template

register = template.Library()

@register.filter(name='currency')
def currency(amount):
    try:
        amount = float(amount)
        return '{:.2f} $'.format(amount)
    except (ValueError, TypeError):
        return 'N/A'

register.filter("currency", currency)
