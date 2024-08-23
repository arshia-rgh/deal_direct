from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user

        return super().create(validated_data)
