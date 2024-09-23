from rest_framework import serializers

from apps.products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Attributes:
        image (ImageField): The image of the product.
        Meta (class): Meta options for the serializer.
    """

    image = serializers.ImageField(required=False)

    class Meta:
        """
        Meta options for ProductSerializer.

        Attributes:
            model (Product): The model to serialize.
            fields (list): The fields to include in the serialization.
            read_only_fields (list): The fields that are read-only.
        """

        model = Product
        fields = [
            "name",
            "description",
            "price",
            "image",
            "category",
            "bought_by",
            "uploaded_by",
        ]
        read_only_fields = [
            "bought_by",
            "uploaded_by",
        ]

    def create(self, validated_data):
        """
            Create a new Product instance.
        **Note**:    Ensures that the uploaded_by will be set to the current user automatically

            Args:
                validated_data (dict): The validated data for the product.

            Returns:
                Product: The created product instance.
        """
        request = self.context.get("request")
        validated_data["uploaded_by"] = request.user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Attributes:
        Meta (class): Meta options for the serializer.
    """

    class Meta:
        """
        Meta options for CategorySerializer.

        Attributes:
            model (Category): The model to serialize.
            fields (str): The fields to include in the serialization.
        """

        model = Category
        fields = "__all__"
