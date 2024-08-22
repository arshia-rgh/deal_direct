from rest_framework import serializers

from products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category"]
        read_only_fields = [
            "bought_by",
            "uploaded_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["uploaded_by"] = request.user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
