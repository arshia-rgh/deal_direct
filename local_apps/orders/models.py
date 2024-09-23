from django.core.exceptions import ValidationError
from django.db import models

from local_apps.accounts.models import User
from local_apps.cart.models import Cart
from local_apps.products.models import Product
from utils.base_model import BaseModel


class Order(BaseModel):
    """
    Model representing an order.

    This model links an order to a cart and tracks the status of the order.
    It provides properties to access the user who placed the order, the products
    in the order, and the total price of the order.
    """

    class OrderStatusChoices(models.TextChoices):
        """
        Choices for the status of an order.
        """

        sending = ("S", "Sending")
        completed = ("C", "Completed")
        waiting_for_payment = ("W", "Waiting For Payment")

    cart = models.OneToOneField(
        to=Cart, on_delete=models.CASCADE, related_name="order", blank=True, null=True
    )
    status = models.CharField(
        max_length=255,
        default=OrderStatusChoices.waiting_for_payment,
        choices=OrderStatusChoices.choices,
    )

    @property
    def user(self):
        """
        Get the user who placed the order.

        Returns:
            User: The user who placed the order.
        """

        return self.cart.user

    @property
    def products(self):
        """
        Get the products in the order.

        Returns:
            list: A list of products in the order.
        """

        return [item.product for item in self.cart.cartitem_set.all()]

    @property
    def total_price(self):
        """
        Calculate the total price of the order.

        Returns:
            float: The total price of the order.
        """

        items = self.cart.cartitem_set.all()

        total = 0

        for item in items:
            total += item.product.price * item.quantity

        return total

    def clean(self):
        """
        Ensure that the cart is not empty unless the order status is completed.
        """

        if self.status != Order.OrderStatusChoices.completed and self.cart is None:
            raise ValidationError(
                "Cart cannot be empty unless the order status is completed."
            )

    def save(self, **kwargs):
        """
        Override the save method to call the clean method before saving.
        """

        self.clean()

        super().save(**kwargs)
