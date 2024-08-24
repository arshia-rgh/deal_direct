import pytest
from django.urls import reverse
from model_bakery import baker

from cart.models import Cart
from products.models import Product


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

    def test_delete_cart(self, api_client, test_user, test_cart):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.delete(reverse("carts:cart-detail"))

        assert response.status_code == 204
        assert not Cart.objects.filter(user=test_user).exists()


@pytest.mark.django_db
class TestCartItemViewSet:
    @pytest.fixture
    def multiple_products(self):
        products = []
        for _ in range(10):
            product = baker.make(Product)
            products.append(product)
        return products

    def test_create_cart_item(
        self, api_client, test_user, test_cart, multiple_products
    ):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("carts:cartitem-list"), data={"product": 1, "quantity": 3}
        )

        assert response.status_code == 201
        assert response.data["cart"] == test_user.cart.id
        assert response.data["product"] == 1
        assert Cart.objects.get(user=test_user).products.filter(id=1).exists()
