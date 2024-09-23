from rest_framework import serializers

from apps.accounts.models import User


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
            "receive_reports",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the authenticated user's profile.

    This serializer handles the retrieval and update of the authenticated user's profile information.

    Fields:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        phone_number (str): The phone number of the user.
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "receive_reports",
            "wallet",
        ]
        read_only_fields = ["wallet"]


class UserPasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing the authenticated user's password.

    This serializer handles the validation of the old password and the new password fields.

    Fields:
        old_password (str): The current password of the user.
        password (str): The new password for the user account.
        confirm_password (str): Confirmation of the new password.

    Methods:
        validate(attrs):
            Validates that the new password and confirm password match.
        validate_old_password(value):
            Validates that the old password is correct.
    """

    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    class Meta:
        model = User

    def validate(self, attrs):
        """
        Validates that the new password and confirm password match.

        Args:
            attrs (dict): The serializer fields and their values.

        Raises:
            serializers.ValidationError: If the passwords do not match.

        Returns:
            dict: The validated attributes.
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                detail={"error": "passwords aren't the same"}
            )
        return attrs

    def validate_old_password(self, value):
        """
        Validates that the old password is correct.

        Args:
            value (str): The old password.

        Raises:
            serializers.ValidationError: If the old password is incorrect.

        Returns:
            str: The validated old password.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                detail={"error": "the old password isn't correct"}
            )
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    Fields:
        email (str): The email address of the user requesting the password reset.
    """

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.

    Fields:
        password (str): The new password for the user account.
    """

    password = serializers.CharField(max_length=255)
