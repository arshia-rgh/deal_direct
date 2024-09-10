from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created", "modified", "total_price"]
    search_fields = ["user__username", "user__email"]
    list_filter = ["created", "modified"]

    def total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.cartitem_set.all()
        )

    total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
