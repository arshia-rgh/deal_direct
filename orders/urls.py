from django.urls import path

from .views import OrderCreateAPIView, OrderPayAPIView, OrderRetrieveDestroyAPIView

app_name = "orders"
urlpatterns = [
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("pay/", OrderPayAPIView.as_view(), name="order-pay"),
    path("detail/", OrderRetrieveDestroyAPIView.as_view(), name="order-detail"),
]
