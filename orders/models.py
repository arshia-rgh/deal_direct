from django.db import models

from accounts.models import User
from cart.models import Cart
from products.models import Product
from utils.base_model import BaseModel


class Order(BaseModel):
    class OrderStatusChoices(models.TextChoices):
        pending = ("P", "Pending")
        completed = ("C", "Completed")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="order")
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(
        default=OrderStatusChoices.pending, choices=OrderStatusChoices.choices
    )

    @property
    def total_price(self):
        items = self.cart.cartitem_set.all()

        total = 0

        for item in items:
            total += item.product.price * item.quantity

        return total
