from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["is_active", "is_staff", "is_superuser"]
