import pytest
from django.core.cache import cache
from django.urls import reverse
from model_bakery import baker

from products.models import Product


@pytest.mark.django_db
class TestProductViewSet:
    @pytest.fixture
    def multiple_products(self):
        products = []
        for _ in range(20):
            product = baker.make(Product)
            products.append(product)
        return products

    def test_list(self, api_client, multiple_products):
        response = api_client.get(reverse("products:product-list"))

        assert response.status_code == 200
        assert len(response.data) == 20

        for product in response.data:
            assert not "id" in product
            assert "name" in product
            assert "price" in product
            assert "uploaded_by" in product
            assert "bought_by" in product

    def test_cacheing_in_list(self, api_client, multiple_products):
        cache_key = "products_list"
        cache.delete(cache_key)

        response = api_client.get(reverse("products:product-list"))

        assert response.status_code == 200

        cached_response = cache.get(cache_key)

        assert cached_response is not None
        assert len(cached_response) == 20

    def test_retrieve(self, api_client, multiple_products):
        response = api_client.get(reverse("products:product-detail", kwargs={"pk": 5}))

        assert response.status_code == 200

        product = Product.objects.get(pk=5)

        assert response.data["name"] == product.name
        assert response.data["uploaded_by"] == product.uploaded_by.id
        assert response.data["category"] == product.category.id

    def test_create_unauthorized_user(self, api_client, test_user, test_category):
        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": "10.00",
                "category": test_category,
            },
        )

        assert response.status_code == 401

    def test_create_success(self, api_client, test_user, test_category):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )

        assert response.status_code == 201
        assert response.data["uploaded_by"] == test_user.id

    def test_delete_product_with_no_owner(
        self, api_client, test_user, test_category, another_test_user
    ):
        test_user.is_active = True
        test_user.save()

        api_client.force_authenticate(test_user)

        response = api_client.post(
            reverse("products:product-list"),
            data={
                "name": "test product",
                "price": 10.00,
                "category": test_category.id,
            },
        )

        assert response.status_code == 201
        assert response.data["uploaded_by"] == test_user.id

        api_client.force_authenticate(another_test_user)

        delete_response = api_client.delete(
            reverse("products:product-detail", kwargs={"pk": 1})
        )

        assert delete_response.status_code == 403
        assert len(Product.objects.all()) == 1


@pytest.mark.django_db
class TestCategoryViewSet:
    pass
