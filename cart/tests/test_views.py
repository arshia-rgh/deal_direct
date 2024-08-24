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

    def test_create_two_carts(self, api_client, test_user):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(reverse("carts:cart"))

        assert response.status_code == 201

        with pytest.raises(Exception):
            response = api_client.post(reverse("carts:cart"))

            assert response.status_code == 400

    def test_create_with_ignored_data(self, api_client, test_user):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(reverse("carts:cart"), data={"products": 1})

        assert response.status_code == 201
        assert response.data["products"] == []


@pytest.mark.django_db
class TestCartRetrieveDestroyAPIView:
    def test_retrieve_cart(self, api_client, test_user, test_cart):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.get(reverse("carts:cart-detail"))

        assert response.status_code == 200
        assert response.data["user"] == test_user.id

    def test_user_can_only_retrieve_owned_cart(
        self, api_client, test_user, test_cart, test_cart_2
    ):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.get(reverse("carts:cart-detail"))

        assert response.status_code == 200
        assert response.data["id"] == 1

    def test_delete_cart(self, api_client, test_user, test_cart):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.delete(reverse("carts:cart-detail"))

        assert response.status_code == 204
        assert not Cart.objects.filter(user=test_user).exists()
