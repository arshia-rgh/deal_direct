import pytest

from cart.models import Cart


@pytest.mark.django_db
class TestCartModel:
    def test_cart_creation(self, test_user):
        cart = Cart.objects.create(user=test_user)

        assert cart.user.username == "testuser"
        assert cart.products.count() == 0
        assert Cart.objects.filter(id=cart.id).exists()
