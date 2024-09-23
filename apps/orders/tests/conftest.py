import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order
from apps.products.models import Product


@pytest.fixture
def test_active_user():
    return User.objects.create_user(
        username="testuser",
        email="test@gmail.com",
        password="testpassword12",
        is_active=True,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_cart(test_active_user):
    return Cart.objects.create(user=test_active_user)


@pytest.fixture
def test_order(test_active_user):
    cart = Cart.objects.create(user=test_active_user)
    product_1 = baker.make(Product, price=10.00)
    product_2 = baker.make(Product, price=20.00)

    CartItem.objects.create(cart=cart, product=product_1, quantity=2)
    CartItem.objects.create(cart=cart, product=product_2, quantity=3)
    # order.total_price = 80.00
    return Order.objects.create(cart=cart)
