from rest_framework import serializers
from .models import Cart, CartItem
from apps.courses.serializers import CourseListSerializer
from apps.coupons.serializers import CouponSerializer
from apps.tiers.serializers import TierSerializer


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseListSerializer()
    tier = TierSerializer()
    coupon = CouponSerializer()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "coupon",
            "referrer",
            "course",
            "tier",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True, source="cartitem_set"
    )  # nombre del related_name o modelname_set

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "total_items",
            "items",
        ]
