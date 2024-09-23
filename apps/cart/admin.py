from django.contrib import admin

from apps.orders.models import Order
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


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ["status", "total_price", "created", "modified"]
    can_delete = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created", "modified", "total_price"]
    search_fields = ["user__username", "user__email"]
    list_filter = ["created", "modified"]
    inlines = [CartItemInline, OrderInline]

    def total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.cartitem_set.all()
        )

    total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product__name",
        "cart__user",
        "quantity",
        "created",
        "modified",
    ]
    search_fields = ["cart__user__username", "cart__user__email", "product__name"]
    list_filter = ["created", "modified"]
    readonly_fields = ["created", "modified"]

    def product__name(self, obj):
        return obj.product.name

    product__name.short_description = "Product Name"

    def cart__user(self, obj):
        return obj.cart.user

    cart__user.short_description = "User (In Cart)"
