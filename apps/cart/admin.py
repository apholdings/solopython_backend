from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_items"]
    search_fields = ["id", "user__username"]
    list_filter = ["user"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "coupon", "referrer", "course"]
    search_fields = ["id", "cart__id", "coupon", "referrer", "course__title"]
    list_filter = ["cart", "course"]
