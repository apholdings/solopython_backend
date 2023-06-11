from rest_framework import serializers
from .models import Post, ViewCount, Heading
from apps.user.serializers import UserSerializer
from apps.category.serializers import CategorySerializer


class ViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCount
        fields = "__all__"


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    view_count = ViewCountSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = "__all__"
