from decimal import Decimal
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from myshop.shop.models import Product


class Cart:
    """
        A shopping cart that stores product items and their quantities.

        The `Cart` class provides methods for adding products to the cart,
        updating the quantities of existing products in the cart, and saving
        the cart to the user's session.

        Usage:
        To use the `Cart` class, first create an instance of the class by
        passing in the `request` object. The `request` object should be the
        request object for the current user's session.

        Example usage:
        cart = Cart(request)

        Methods:
        - `add(product, quantity=1, update_quantity=False)`: Adds a product
        to the cart or updates the quantity of an existing product in the
        cart. The `product` argument should be an instance of a Product model.
        The `quantity` argument is the quantity of the product to add to the
        cart, and the `update_quantity` argument determines whether to update
        the quantity of an existing product in the cart or add a new product.
        - `save()`: Saves the cart to the user's session.
        - `remove(product)`: Removes the product from the shopping cart.
        - `get_total_price()`: Returns the total price of all products in the cart.
        - `clear()`: Removes all items from the cart.

        Properties:
        - `__len__()`: Returns the total number of products in the cart.
        - `__iter__(product)`: Iterates through the user's shopping cart and retrieves products from the database.
    """

    def __init__(self, request: SessionBase) -> None:
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def __iter__(self, product):
        """
        Iterates through the user's shopping cart and retrieves products from the database.
        """
        product_ids = self.cart.keys()
        products = Product.object.filter(id__in=product_ids)
        cart = self.cart.copy()

        for products in products:
            product = cart[str(product.id)['product']]
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Calculating the number of all products in the shopping cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def save(self) -> None:
        # Marks the session as "modified" to make sure it is saved.
        self.session.modified = True

    def add(self, product: object, quantity: int = 1, update_quantity: bool = False) -> None:
        """
        Adds the product to the cart or updates the quantity.
        """
        if not product:
            raise ValueError("Product cannot be None")

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Removes the product from the shopping cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove the shopping cart from the current session.
        del self.session[self.CART_SESSION_ID]
        self.save()
