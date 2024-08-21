from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending the default Django AbstractUser.

    Attributes:
        email (EmailField): The user's email address, which must be unique.
        phone_number (CharField): The user's phone number, which is optional and must be unique if provided.
        is_active (BooleanField): Indicates whether the user account is active.
         (Based on if the user confirmed his email)
    """

    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)
