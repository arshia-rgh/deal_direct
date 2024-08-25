from rest_framework import serializers

from cart.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.

    This serializer handles the serialization and deserialization of Cart objects.
    It includes all fields of the Cart model and sets the 'user' field as read-only.
    """

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, attrs):
        request = self.context["request"]

        if Cart.objects.filter(user=request.user):
            raise serializers.ValidationError("Each user can have one cart at moment")

        return attrs

    def create(self, validated_data):
        """
        Create a new Cart instance.

        This method sets the 'user' field to the current user from the request context.

        Args:
            validated_data (dict): The validated data for creating the Cart instance.

        Returns:
            Cart: The created Cart instance.
        """

        request = self.context["request"]
        validated_data["user"] = request.user

        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    This serializer handles the serialization and deserialization of CartItem objects.
    It includes all fields of the CartItem model and sets the 'cart' field as read-only.
    """

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["cart"]

    def create(self, validated_data):
        """
        Create a new CartItem instance.

        This method sets the 'cart' field to the current user's cart from the request context.

        Args:
            validated_data (dict): The validated data for creating the CartItem instance.

        Returns:
            CartItem: The created CartItem instance.
        """

        request = self.context["request"]
        validated_data["cart"] = request.user.cart
        return super().create(validated_data)
