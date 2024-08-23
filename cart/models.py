from django.db import models

from accounts.models import User
from products.models import Product
from utils.base_model import BaseModel


class Cart(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(to=Product, through="CartItem")


class CartItem(BaseModel):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
