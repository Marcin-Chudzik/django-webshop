from django.shortcuts import render
from django.db import transaction
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    """
    GET: Displays the empty form to make an order.
    POST: Checking the form's data validation and creating the OrderItem object for each item in the session cart.
          Using the database transaction.atomic() to make sure that the OrderItem will be inserted into the database
          only if all order items will be valid.
    """
    cart = Cart(request)

    if request.method == 'POST' and cart.__len__() > 0:
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_items = [
                OrderItem(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                for item in cart
            ]
            with transaction.atomic():
                # Using bulk_create() to insert all order_items as one query.
                OrderItem.objects.bulk_create(order_items)
            # Deleting the products from the session cart.
            cart.clear()
            # Running the asynchronous task for send email to the client.
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
