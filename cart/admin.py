from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ("product", "quantity", "price", "total")
    can_delete = False

    def price(self, obj):
        return obj.product.price

    price.short_description = "Price"

    def total(self, obj):
        return obj.product.price * obj.quantity

    total.short_description = "Total"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created", "modified", "total_price"]
    search_fields = ["user__username", "user__email"]
    list_filter = ["created", "modified"]
    inlines = [CartItemInline]

    def total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.cartitem_set.all()
        )

    total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
