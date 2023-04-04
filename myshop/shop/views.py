from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Product, Category


def product_list(request, category_slug=None):
    """
    View function that displays a list of products, optionally filtered by category.

    Args:
        category_slug: (optional) string representing the slug of a Category object to filter by.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'products': products})


def product_detail(request, product_id, slug):
    """
    View function that displays the details of a single product.

    Args:
        product_id: integer representing the ID of the Product object to display.
        slug: string representing the slug of the Product object to display.
    """
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    form = CartAddProductForm()

    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': form})
