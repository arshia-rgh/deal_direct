from django.core.cache import cache

import pytest
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


@pytest.mark.django_db
class TestCategoryViewSet:
    pass
