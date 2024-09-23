from celery import shared_task

from local_apps.orders.models import Order


@shared_task
def delete_cart_after_7_days(order_id):
    try:
        order = Order.objects.get(id=order_id)
        cart = order.cart

        order.cart = None
        cart.delete()
        order.status = Order.OrderStatusChoices.completed
        order.save()
    except Order.DoesNotExist:
        pass
