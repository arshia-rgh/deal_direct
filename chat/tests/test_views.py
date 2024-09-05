import pytest
from django.urls import reverse

from chat.models import ChatRoom


@pytest.mark.django_db
class TestChatRoomViewSet:
    def test_create_new_chat_room(self, api_client, test_product, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(
            reverse("chats:chatroom-list"), data={"product": test_product.id}
        )

        assert response.status_code == 201
        assert ChatRoom.objects.all().count() == 1
        assert (
            ChatRoom.objects.get(product=test_product).name
            == f"{test_product.name} - Seller: {test_product.uploaded_by.username}"
        )

        assert (
            test_active_user
            in ChatRoom.objects.get(product=test_product).participants.all()
        )
