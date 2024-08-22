from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import (
    UserRegisterSerializer,
    UserProfileSerializer,
    UserPasswordChangeSerializer,
)
from .permissions import IsAuthenticatedAndActive
from .tasks import update_bonus_wallet_amount_when_verified


class UserRegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view handles the creation of a new user. Upon successful registration,
    it sends a message to the user to check their email for account activation.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Create a new user and send a message to check the email for account activation.

        Args:
            request (Request): The DRF request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object containing a success message and HTTP status code 201.
        """

        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "User registered successfully, please check your email to active your account"
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    """
    View that handles email verification
    """

    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Verifies the user's email.

        Args:
            request (Request): The DRF request object.
            uidb64 (str): The base64 encoded user ID.
            token (str): The token for email verification.

        Returns:
            Response: A response object containing a success or failure message.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            update_bonus_wallet_amount_when_verified.delay(user.id)
            return Response(
                {
                    "message": "Email verified successfully. A bonus will be added to your wallet soon"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the authenticated user's profile.

    This view allows the authenticated user to retrieve and update their own profile information.
    It uses the `UserProfileSerializer` for serialization and the `IsAuthenticatedAndActive`
    permission class to ensure that only authenticated and active users can access this view.
    """

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedAndActive,)

    def get_object(self):
        """
        Retrieve the authenticated user's profile.

        Returns:
            User: The authenticated user.
        """
        return self.request.user


class UserPasswordChangeView(generics.UpdateAPIView):
    """
    API view for changing the authenticated user's password.

    This view allows the authenticated user to change their password. It uses the
    `UserPasswordChangeSerializer` for validation and the `IsAuthenticatedAndActive`
    permission class to ensure that only authenticated and active users can access this view.
    """

    serializer_class = UserPasswordChangeSerializer
    permission_classes = (IsAuthenticatedAndActive,)

    def get_object(self):
        """
        Retrieve the authenticated user.

        Returns:
            User: The authenticated user.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Update the authenticated user's password.

        Args:
            request (Request): The DRF request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object containing a success message and HTTP status code 200.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data["password"])
        self.object.save()
        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )
