from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import IncreaseWalletSerializer
from accounts.tasks import update_wallet_balance
from .zarinpal import send_request, verify
from ..permissions import IsAuthenticatedAndActive


class IncreaseWalletAPIView(APIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def post(self, request):
        user = request.user
        serializer = IncreaseWalletSerializer(data=request.data)

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


class VerifyDepositAPIView(APIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def post(self, request):
        authority = request.data.get("Authority")
        amount = request.data.get("Amount")
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
                {"status": "Payment verified successfully", "RefID": response["RefID"]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Payment verification failed", "code": response["code"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
