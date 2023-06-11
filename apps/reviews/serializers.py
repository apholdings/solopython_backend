from rest_framework import serializers
from .models import *
from apps.user.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "date_created",
        ]
