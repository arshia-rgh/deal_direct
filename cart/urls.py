from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet, CartCreateApiView, CartRetrieveDestroyAPIView

router = DefaultRouter()

router.register("cart-items", CartItemViewSet)

app_name = "carts"
urlpatterns = [
    path("", include(router.urls)),
    path("carts/", CartCreateApiView.as_view(), name="cart"),
    path("carts/detail/", CartRetrieveDestroyAPIView.as_view(), name="cart-detail"),
]
