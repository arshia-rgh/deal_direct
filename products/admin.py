from django.contrib import admin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category_name", "created", "modified"]
    readonly_fields = ["created", "modified"]

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = "Category"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
