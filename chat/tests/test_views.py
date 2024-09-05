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

        assert (
            test_product.uploaded_by
            in ChatRoom.objects.get(product=test_product).participants.all()
        )

    def test_delete_chat_room(self, api_client, test_active_user, test_product):
        chat_room = ChatRoom.objects.create(product=test_product)
        assert ChatRoom.objects.all().count() == 1

        api_client.force_authenticate(test_active_user)

        # test if the user isn't the participant of this chat room (must 404)
        response = api_client.delete(
            reverse("chats:chatroom-detail", kwargs={"pk": chat_room.id})
        )

        assert response.status_code == 404

        # add user as a participant of the chat room
        chat_room.participants.add(test_active_user)

        response = api_client.delete(
            reverse("chats:chatroom-detail", kwargs={"pk": chat_room.id})
        )

        assert response.status_code == 204
        assert not ChatRoom.objects.filter(id=chat_room.id).exists()
