from django.contrib import admin

from chat.models import ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "product__name", "get_participants"]
    filter_horizontal = ["participants"]

    def product__name(self, obj):
        return obj.product.name

    product__name.short_description = "Product Name"

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])

    get_participants.short_description = "Participants"
