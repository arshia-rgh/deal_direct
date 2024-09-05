import pytest
from model_bakery import baker

from products.models import Product


@pytest.fixture
def test_product():
    product = baker.make(Product)

    return product
