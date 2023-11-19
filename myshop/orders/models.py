from django.db import models
from shop.models import Product


class Order(models.Model):
    """
    A model representing an order.

    Attributes:
        first_name (CharField): The first name of the customer.
        last_name (CharField): The last name of the customer.
        email (EmailField): The email address of the customer.
        address (CharField): The address of the customer.
        postal_code (CharField): The postal code of the customer's address.
        city (CharField): The city of the customer's address.
        created (DateTimeField): The date and time when the order was created.
        updated (DateTimeField): The date and time when the order was last updated.
        paid (BooleanField): A flag indicating whether the order has been paid.

    Meta:
        ordering (tuple): A tuple specifying the default ordering for queries.

    Methods:
        __str__: Returns a string representation of the order.
        get_total_cost: Calculates and returns the total cost of the order.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    A model representing an item in an order.

    Attributes:
        order (ForeignKey): The order this item belongs to.
        product (ForeignKey): The product being ordered.
        price (DecimalField): The price of the product.
        quantity (PositiveIntegerField): The quantity of the product being ordered.

    Methods:
        __str__: Returns a string representation of the order item.
        get_cost: Calculates and returns the total cost of the order item.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
