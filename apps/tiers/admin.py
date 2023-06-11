from django.contrib import admin
from .models import *


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = (
        "tier_id",
        "reason",
        "frequency",
        "billing_day",
        "transaction_amount",
    )
    search_fields = ("tier_id", "reason")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "vendor", "tier", "status", "next_payment_date")
    search_fields = ("subscriber__username", "vendor__username", "tier__reason")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "highlight",
    )
    search_fields = ("title", "highlight")
