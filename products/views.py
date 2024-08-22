from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting products.

    - Any user (even anonymous) can view the list of products or retrieve a product.
    - Only authenticated users can create a product.
    - Only the user who uploaded the product can update or delete it.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting categories.

    - Any user (even anonymous) can view the list of categories or retrieve a category.
    - Only authenticated users can create, update, or delete a category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
