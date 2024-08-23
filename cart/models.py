from django.db import models

from accounts.models import User
from utils.base_model import BaseModel
from products.models import Product


class Cart(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(to=Product, through="CartItem")
