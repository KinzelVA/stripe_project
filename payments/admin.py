from django.contrib import admin
from .models import Item, Order  # Импортируем модели

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    search_fields = ("name", "description")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_amount", "created_at")
    filter_horizontal = ("items",)

