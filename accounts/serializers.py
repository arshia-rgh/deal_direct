from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    This serializer handles the creation of a new user by taking in the necessary
    fields and creating a user instance with the provided data.

    Fields:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password for the user account.
        phone_number (str): The phone number of the user.

    Methods:
        create(validated_data):
            Creates and returns a new user instance with the validated data.
        **Note**: (override to make sure the password will be hashed)
    """

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
        ]
        read_only_fields = [
            "password",
        ]
