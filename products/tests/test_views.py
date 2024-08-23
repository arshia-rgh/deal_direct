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


@pytest.mark.django_db
class TestCategoryViewSet:
    pass
