from rest_framework import serializers
from .models import FixedPriceCoupon, PercentageCoupon, Coupon


class FixedPriceCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedPriceCoupon
        fields = ("id", "discount_price", "uses")


class PercentageCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageCoupon
        fields = ("id", "discount_percentage", "uses")


class CouponSerializer(serializers.ModelSerializer):
    fixed_price_coupon = FixedPriceCouponSerializer(required=False)
    percentage_coupon = PercentageCouponSerializer(required=False)
    content_type = serializers.CharField(read_only=True)

    class Meta:
        model = Coupon
        fields = (
            "id",
            "name",
            "user",
            "fixed_price_coupon",
            "percentage_coupon",
            "content_type",
        )
