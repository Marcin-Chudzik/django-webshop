from myshop.utils import logger
from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id: int) -> int:
    """
      Asynchronous Celery task for sending an order confirmation email to a customer.

      Args:
          order_id (int): The ID of the order to send the confirmation email for.

      Returns:
          int: The number of emails sent (1 if successful, 0 otherwise).
    """
    order = Order.objects.filter(id=order_id).first()
    if not order:
        # handle case where order is not found.
        logger.error(f"function: order_created -> Order with ID {order_id} not found.")
        return 0

    subject = f"MyShop - Order {order.id}"
    message = f"Welcome, {order.first_name}.\n\nYou made an order in our shop.\n\nYour order ID is, {order_id}"
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])

    if not mail_sent:
        # handle case where email failed to send.
        logger.error(f"function: order_created -> Failed to send confirmation email for order {order_id}")

    return mail_sent
