from django.urls import path

from .views import OrderCreateAPIView

urlpatterns = [
    path("create/", OrderCreateAPIView.as_view(), name="create-order"),
]
