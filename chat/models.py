from django.db import models

from accounts.models import User
from utils.base_model import BaseModel


class ChatRoom(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(
        to="Product", on_delete=models.CASCADE, related_name="room"
    )
    participants = models.ManyToManyField(to=User, related_name="rooms")

    def save(self, **kwargs):
        if not self.name:
            self.name = (
                f"{self.product.name} - Seller: {self.product.uploaded_by.username}"
            )

        super().save(**kwargs)
