from django.db import models

from accounts.models import User
from utils.base_model import BaseModel


class ChatRoom(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(to=User, related_name="rooms")

    def save(self, **kwargs):
        if not self.name:
            participant_names = [user.username for user in self.participants.all()]
            self.name = "_".join(participant_names)

        super().save(**kwargs)

    def add_participants(self, user):
        if self.participants.count() >= 2:
            raise ValueError("A room cannot have more than 2 participants.")
        self.participants.add(user)
