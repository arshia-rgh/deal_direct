from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from local_apps.accounts.serializers.payment_serializers import (
    IncreaseWalletSerializer,
    VerifyDepositSerializer,
)
from local_apps.accounts.tasks import update_wallet_balance
from utils.mixins import ThrottleMixin, LoggingMixin
from .zarinpal import send_request, verify
from ..permissions import IsAuthenticatedAndActive


class IncreaseWalletAPIView(ThrottleMixin, generics.GenericAPIView):
    """
    API view for increasing the user's wallet balance.

    This view handles the request to deposit an amount into the user's wallet.
    It uses the `IncreaseWalletSerializer` for validation and the `IsAuthenticatedAndActive`
    permission class to ensure that only authenticated and active users can access this view.
    """

    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = IncreaseWalletSerializer

    def post(self, request):
        """
        Handle the POST request to deposit an amount into the user's wallet.

        Args:
            request (Request): The HTTP request object containing the deposit details.

        Returns:
            HttpResponseRedirect: Redirects to the payment gateway URL if the request is successful.
            Response: A response object containing an error message and HTTP status code 400 if the request fails.
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            response = send_request(
                request,
                amount,
                "Deposit Wallet",
                user.phone_number,
                user.email,
            )

            if response["status"]:
                return HttpResponseRedirect(response["url"])
            else:
                return Response(
                    {"error": "Payment request failed", "code": response["code"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyDepositAPIView(ThrottleMixin, LoggingMixin, generics.GenericAPIView):
    """
    API view for verifying a wallet deposit.

    This view handles the request to verify a deposit into the user's wallet.
    It uses the `IsAuthenticatedAndActive` permission class to ensure that only authenticated
    and active users can access this view.
    """

    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = VerifyDepositSerializer

    def post(self, request):
        """
        Handle the POST request to verify a deposit into the user's wallet.

        Args:
            request (Request): The HTTP request object containing the verification details.

        Returns:
            Response: A response object containing a success message and HTTP status code 200 if the verification is successful.
            Response: A response object containing an error message and HTTP status code 400 if the verification fails.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            authority = serializer.validated_data.get("Authority")
            amount = serializer.validated_data.get("Amount")
            if not amount or not authority:
                return Response(
                    {"error": "Authority and Amount are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            response = verify(amount, authority)
            if response["status"]:
                user = request.user
                update_wallet_balance.delay(user.id, amount)

                return Response(
                    {
                        "status": "Payment verified successfully",
                        "RefID": response["RefID"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Payment verification failed", "code": response["code"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
