from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product_names", "total_price", "status"]

    def product_names(self, obj):
        return ", ".join([product.name for product in obj.products])

    product_names.short_description = "Product Names"
