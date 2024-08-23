import pytest

from products.models import Product


@pytest.mark.django_db
class TestProductModel:
    def test_production_creation(self, test_product):
        assert test_product.name == "test product name"
        assert Product.objects.filter(name="test product name").exists()

    def test_product_creation_invalid_data(self):
        with pytest.raises(Exception):
            Product.objects.create(name="", description="", image="invalid image")

    def test_product_update(self, test_product):
        test_product.name = "test name 2"
        test_product.save()

        assert test_product.name == "test name 2"

    def test_product_delete(self, test_product):
        test_product.delete()

        assert not Product.objects.filter(name="test product name").exists()
