import pytest
from django.urls import reverse

from accounts.models import User
from chat.models import ChatRoom
from chat.tests.conftest import api_client


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

    def test_get_chat_room(self, api_client, test_active_user, test_product):
        chat_room = ChatRoom.objects.create(product=test_product)
        chat_room.participants.add(test_active_user)

        api_client.force_authenticate(test_active_user)

        response = api_client.get(
            reverse("chats:chatroom-detail", kwargs={"pk": chat_room.id})
        )

        assert response.status_code == 200
        assert response.data["id"] == chat_room.id


@pytest.mark.django_db
class TestAccessChatRoomView:
    def test_access_chat_room_view_authenticated(
        self, api_client, test_product, test_active_user
    ):
        chat_room = ChatRoom.objects.create(product=test_product)
        chat_room.participants.add(test_active_user)
        api_client.force_login(test_active_user)

        response = api_client.get(
            reverse("chats:access-chat", kwargs={"room_name": chat_room.name})
        )

        assert response.status_code == 200
        assert "room_name" in response.context
        assert response.context["room_name"] == chat_room.name

    def test_access_chat_room_view_unauthenticated(self, api_client, test_product):
        chat_room = ChatRoom.objects.create(product=test_product)

        response = api_client.get(
            reverse("chats:access-chat", kwargs={"room_name": chat_room.name})
        )

        assert response.status_code == 302  # Redirect to login page

    def test_access_chat_room_view_not_participant(self, api_client, test_product):
        chat_room = ChatRoom.objects.create(product=test_product)
        non_participant_user = User.objects.create_user(
            username="nonparticipant", password="testpass", is_active=True
        )
        api_client.force_login(non_participant_user)

        response = api_client.get(
            reverse("chats:access-chat", kwargs={"room_name": chat_room.name})
        )

        assert response.status_code == 403  # Forbidden
