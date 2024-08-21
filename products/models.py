from utils.base_model import BaseModel
from django.db import models


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="img/products/")
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
