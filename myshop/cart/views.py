from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    # Displays the details of the products currently in the session cart.
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update_quantity': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@require_http_methods(['POST'])
def cart_add(request, product_id):
    """
    View function that adds a product to the cart and redirects to the cart detail page.

    Args:
        product_id: integer representing the ID of the Product object to display.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update_quantity'])
    return redirect('cart:cart_detail')


@require_http_methods(['POST'])
def cart_remove(request, product_id):
    """
    Removes a product from the session cart and redirects the user to the cart detail page.

    Args:
        product_id: integer representing the ID of the Product object to display.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
