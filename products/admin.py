from django.contrib import admin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "price",
        "category_name",
        "created",
        "modified",
        "uploaded_by_username",
        "bought_by_username",
    ]
    readonly_fields = ["created", "modified"]
    search_fields = [
        "uploaded_by__username",
        "bought_by__username",
        "uploaded_by__email",
        "bought_by__email",
    ]
    list_filter = ["created", "modified", "category"]

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = "Category"

    def uploaded_by_username(self, obj):
        return obj.uploaded_by.username

    uploaded_by_username.short_description = "Seller"

    def bought_by_username(self, obj):
        try:
            return obj.bought_by.username
        except Exception:
            return None

    bought_by_username.short_description = "Buyer"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
