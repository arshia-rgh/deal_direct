from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet

router = DefaultRouter()

router.register("cart-items", CartItemViewSet)

app_name = "carts"
urlpatterns = [
    path("", include(router.urls)),
]
