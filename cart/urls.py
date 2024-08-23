from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet, CartItemViewSet

router = DefaultRouter()

router.register("carts", CartViewSet)
router.register("cart-items", CartItemViewSet)

app_name = "carts"
urlpatterns = [
    path("", include(router.urls)),
]
