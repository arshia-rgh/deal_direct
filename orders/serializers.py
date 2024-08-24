from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["cart", "status", "created"]
        read_only_fields = ["cart", "status", "created"]

    def create(self, validated_data):
        request = self.context["request"]

        validated_data["cart"] = request.user.cart

        return super().create(validated_data)
