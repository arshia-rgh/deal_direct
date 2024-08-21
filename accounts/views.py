from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserRegisterSerializer


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
            return Response(
                {"message": "Email verified successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView:
    pass
