from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "phone_number",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
