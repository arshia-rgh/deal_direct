from django.db import models

from apps.accounts.models import User
from utils.base_model import BaseModel


class Product(BaseModel):
    """
    Represents a product in the system.

    Attributes:
        name (str): The name of the product. (unique)
        description (str): A detailed description of the product.
        price (Decimal): The price of the product.
        image (ImageField): An image of the product.
        category (ForeignKey): The category to which the product belongs.
        uploaded_by (ForeignKey): The user who uploaded the product.
        bought_by (ForeignKey): The user who bought the product (nullable).
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="img/products/", null=True, blank=True)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)

    uploaded_by = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="uploaded_products"
    )
    bought_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="bought_products",
        null=True,
        blank=True,
        default=None,
    )


class Category(BaseModel):
    """
    Represents a category of products.

    Attributes:
        name (str): The name of the category. (unique)
        description (str): A detailed description of the category.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
