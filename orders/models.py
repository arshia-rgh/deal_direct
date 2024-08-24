from django.db import models

from accounts.models import User
from cart.models import Cart
from products.models import Product
from utils.base_model import BaseModel


class Order(BaseModel):
    class OrderStatusChoices(models.TextChoices):
        sending = ("S", "Sending")
        completed = ("C", "Completed")
        waiting_for_payment = ("W", "Waiting For Payment")

    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(
        max_length=255,
        default=OrderStatusChoices.waiting_for_payment,
        choices=OrderStatusChoices.choices,
    )

    @property
    def user(self):
        return self.cart.user

    @property
    def products(self):
        return [item.product for item in self.cart.cartitem_set.all()]

    @property
    def total_price(self):
        items = self.cart.cartitem_set.all()

        total = 0

        for item in items:
            total += item.product.price * item.quantity

        return total
