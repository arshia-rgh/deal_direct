from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import IncreaseWalletSerializer
from .zarinpal import send_request
from ..permissions import IsAuthenticatedAndActive


class IncreaseWalletAPIView(APIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def post(self, request):
        user = self.request.user
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
    pass
