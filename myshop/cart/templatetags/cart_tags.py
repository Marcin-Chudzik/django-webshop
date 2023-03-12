from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart_amount(context):
    request = context['request']
    cart = request.session.get(settings.CART_SESSION_ID, {})
    return sum([item['quantity'] for item in cart.values()])

