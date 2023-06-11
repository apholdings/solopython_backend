from rest_framework import serializers
from .models import *
from apps.user.serializers import UserSerializer


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "title", "highlight"]


class TierSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Tier
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "mostPopular",
            "features",
            "tier_id",
            "application_id",
            "collector_id",
            "external_reference",
            "init_point",
            "date_created",
            "last_modified",
            "reason",
            "frequency",
            "frequency_type",
            "repetitions",
            "billing_day",
            "billing_day_proportional",
            "free_trial_frequency",
            "free_trial_frequency_type",
            "transaction_amount",
            "transaction_amount_proportional",
            "currency_id",
            "payment_methods_allowed",
            "back_url",
            "status",
            "thumbnail",
            "index",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    vendor = UserSerializer()
    tier = TierSerializer()

    class Meta:
        model = Subscription
        fields = "__all__"
