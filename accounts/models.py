from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        unique=True,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)
