import pytest
from django.urls import reverse

from cart.models import Cart


@pytest.mark.django_db
class TestCartCreateAPIView:
    def test_create_cart_authenticated_user(self, api_client, test_user):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(reverse("carts:cart"))

        assert response.status_code == 201
        assert Cart.objects.all().count() == 1
        assert response.data["products"] == []
        assert response.data["user"] == test_user.id
