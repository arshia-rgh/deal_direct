from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer handles the validation and creation of Order instances.
    It ensures that an order is not created if one already exists for the user's cart.
    """

    class Meta:
        model = Order
        fields = ["cart", "status", "created"]
        read_only_fields = ["cart", "status", "created"]

    def validate(self, data):
        """
        Validate the order data.

        This method checks if an order already exists for the user's cart.
        If an order exists, it raises a ValidationError.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If an order already exists for the user's cart.
        """

        request = self.context["request"]
        cart = request.user.cart

        if Order.objects.filter(cart=cart).exists():
            raise serializers.ValidationError("An order already exists for this cart.")

        return data

    def create(self, validated_data):
        """
        Create a new order instance.

        This method sets the cart to the user's cart before creating the order.

        Args:
            validated_data (dict): The validated data for creating the order.

        Returns:
            Order: The created order instance.
        """

        request = self.context["request"]

        validated_data["cart"] = request.user.cart

        return super().create(validated_data)
