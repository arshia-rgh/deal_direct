import pytest

from apps.accounts.models import User
from apps.chat.models import ChatRoom


@pytest.mark.django_db
class TestChatRoomModel:
    def test_create_new_instance_successfully(self, test_product):
        instance = ChatRoom.objects.create(product=test_product)

        assert ChatRoom.objects.all().count() == 1
        assert instance.name is not None

    def test_new_custom_save_logic(self, test_product):
        instance = ChatRoom.objects.create(product=test_product)

        assert (
            instance.name
            == f"{test_product.name} - Seller: {test_product.uploaded_by.username}"
        )
        assert instance.product == test_product

    def test_add_participant(self, test_product):
        instance = ChatRoom.objects.create(product=test_product)
        user = User.objects.create_user(username="testuser", password="testpass")
        instance.participants.add(user)

        assert user in instance.participants.all()

    def test_remove_participant(self, test_product):
        instance = ChatRoom.objects.create(product=test_product)
        user = User.objects.create_user(username="testuser", password="testpass")
        instance.participants.add(user)

        assert user in instance.participants.all()

        instance.participants.remove(user)

        assert user not in instance.participants.all()
