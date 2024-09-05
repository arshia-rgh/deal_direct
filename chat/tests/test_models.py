import pytest
from chat.models import ChatRoom


@pytest.mark.django_db
class TestChatRoomModel:
    def test_create_new_instance_successfully(self, test_product):
        instance = ChatRoom.objects.create(product=test_product)

        assert ChatRoom.objects.all().count() == 1
        assert instance.name is not None
