import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from accounts.models import User
from cart.models import Cart, CartItem
from orders.models import Order
from products.models import Product


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
def multiple_products():
    products = []
    for _ in range(5):
        product = baker.make(Product)
        products.append(product)
    return products


@pytest.fixture
def multiple_cart_items(multiple_products, test_cart):
    cart_item_list = []
    for product in multiple_products:
        cart_item = CartItem.objects.create(cart=test_cart, product=product, quantity=3)
        cart_item_list.append(cart_item)

    return cart_item_list


@pytest.fixture
def test_order(test_active_user):
    cart = Cart.objects.create(user=test_active_user)
    product_1 = baker.make(Product, price=10.00)
    product_2 = baker.make(Product, price=20.00)

    CartItem.objects.create(cart=cart, product=product_1, quantity=2)
    CartItem.objects.create(cart=cart, product=product_2, quantity=3)
    # order.total_price = 80.00
    return Order.objects.create(cart=cart)
