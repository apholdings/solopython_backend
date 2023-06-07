from django.contrib import admin
from .models import Coupon, FixedPriceCoupon, PercentageCoupon


class FixedPriceCouponAdmin(admin.ModelAdmin):
    list_display = ["id", "discount_price", "uses"]


admin.site.register(FixedPriceCoupon, FixedPriceCouponAdmin)


class PercentageCouponAdmin(admin.ModelAdmin):
    list_display = ["id", "discount_percentage", "uses"]


admin.site.register(PercentageCoupon, PercentageCouponAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "user",
        "fixed_price_coupon",
        "percentage_coupon",
        "content_type",
    ]
    list_filter = ["content_type"]
    search_fields = ["name"]


admin.site.register(Coupon, CouponAdmin)
