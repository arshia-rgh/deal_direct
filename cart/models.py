from django.db import models

from accounts.models import User
from products.models import Product
from utils.base_model import BaseModel


class Cart(BaseModel):
    """
    Represents a shopping cart for a user.

    Attributes:
        user (User): The user who owns the cart.
        products (ManyToManyField): The products in the cart, through the CartItem model.
    """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(to=Product, through="CartItem")


class CartItem(BaseModel):
    """
    Represents an item in a shopping cart.

    Attributes:
        product (Product): The product in the cart item.
        cart (Cart): The cart to which the item belongs.
        quantity (int): The quantity of the product in the cart item.
    """

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
