from django.db import models

from accounts.models import User
from utils.base_model import BaseModel


class ChatRoom(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(to=User, related_name="rooms")
