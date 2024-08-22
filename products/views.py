from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.models import Product
from products.serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Any user (even anonymous) can view the list of products or retrieve a product.
    # Only authenticated users can create a product.
    # Only the user who uploaded the product can update or delete it.
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
