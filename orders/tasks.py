from celery import shared_task

from orders.models import Order


@shared_task
def delete_cart_after_7_days(order_id):
    try:
        order = Order.objects.get(id=order_id)
        cart = order.cart
        pass
    except:
        pass
    # TODO implement later
