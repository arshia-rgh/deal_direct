from rest_framework import serializers


class IncreaseWalletSerializer(serializers.Serializer):
    """
    Serializer for increasing the user's wallet balance.

    Fields:
        amount (Decimal): The amount to increase the wallet balance by.
    """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class VerifyDepositSerializer(serializers.Serializer):
    """
    Serializer for verifying a wallet deposit.

    Fields:
        authority (str): The authority code for the deposit transaction.
        amount (Decimal): The amount deposited into the user's wallet.
    """

    authority = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
