from django.core.cache import cache

import pytest
from django.urls import reverse
from model_bakery import baker

from cart.models import Cart
from products.models import Product


@pytest.mark.django_db
class TestCartCreateAPIView:
    def test_create_cart_authenticated_user(self, api_client, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(reverse("carts:cart"))

        assert response.status_code == 201
        assert Cart.objects.all().count() == 1
        assert response.data["products"] == []
        assert response.data["user"] == test_active_user.id
        assert Cart.objects.get(user=test_active_user).user == test_active_user
        assert Cart.objects.get(user=test_active_user).products.count() == 0

    def test_create_two_carts(self, api_client, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(reverse("carts:cart"))

        assert response.status_code == 201

        with pytest.raises(Exception):
            response = api_client.post(reverse("carts:cart"))

            assert response.status_code == 400

    def test_create_with_ignored_data(self, api_client, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(reverse("carts:cart"), data={"products": 1})

        assert response.status_code == 201
        assert response.data["products"] == []


@pytest.mark.django_db
class TestCartRetrieveDestroyAPIView:
    def test_retrieve_cart(self, api_client, test_active_user, test_cart):
        api_client.force_authenticate(test_active_user)

        response = api_client.get(reverse("carts:cart-detail"))

        assert response.status_code == 200
        assert response.data["user"] == test_active_user.id

    def test_delete_cart(self, api_client, test_active_user, test_cart):
        api_client.force_authenticate(test_active_user)

        response = api_client.delete(reverse("carts:cart-detail"))

        assert response.status_code == 204
        assert not Cart.objects.filter(user=test_active_user).exists()


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
        self, api_client, test_active_user, test_cart, multiple_products
    ):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(
            reverse("carts:cartitem-list"), data={"product": 1, "quantity": 3}
        )

        assert response.status_code == 201
        assert response.data["cart"] == test_active_user.cart.id
        assert response.data["product"] == 1
        assert Cart.objects.get(user=test_active_user).products.filter(id=1).exists()
        assert (
            Cart.objects.get(user=test_active_user)
            .products.get(id=1)
            .cartitem_set.first()
            .quantity
            == 3
        )

    def test_get_all_cart_items(
        self, api_client, test_active_user, test_cart, multiple_products
    ):
        api_client.force_authenticate(test_active_user)

        # add some cart items to the test_active_user cart
        for product in multiple_products[:5]:
            response = api_client.post(
                reverse("carts:cartitem-list"),
                data={"product": product.id, "quantity": 3},
            )
            assert response.status_code == 201

        response = api_client.get(reverse("carts:cartitem-list"))

        assert response.status_code == 200
        assert len(response.data) == 5

        assert len(Cart.objects.get(user=test_active_user).products.all()) == 5

    def test_cache_list(
        self, api_client, test_active_user, multiple_products, test_cart
    ):
        cache_key = "cart_items_list"
        cache.delete(cache_key)

        cache_response = cache.get(cache_key)
        assert cache_response is None

        api_client.force_authenticate(test_active_user)

        # add some cart items to the test_active_user cart
        for product in multiple_products[:5]:
            response = api_client.post(
                reverse("carts:cartitem-list"),
                data={"product": product.id, "quantity": 3},
            )
            assert response.status_code == 201

        response = api_client.get(reverse("carts:cartitem-list"))

        assert response.status_code == 200

        cache_response = cache.get(cache_key)

        assert cache_response is not None
        assert len(cache_response) == 5
