from django import template
from ..cart import Cart

register = template.Library()


@register.simple_tag(takes_context=True)
def get_cart(context):
    request = context.get('request')
    cart = Cart(request) if request else {}
    return cart
