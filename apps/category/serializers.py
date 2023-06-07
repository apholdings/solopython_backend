from .models import *
from rest_framework import serializers


class ViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCount
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    category_view_count = ViewCountSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
