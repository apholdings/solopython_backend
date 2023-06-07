from rest_framework import serializers
from .models import *
from apps.user.serializers import UserSerializer
from apps.category.serializers import CategorySerializer


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = ["id", "address"]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "position_id",
            "title",
            "file",
            "media_type",
            "course",
        ]


class CourseListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    sellers = SellersSerializer(many=True)
    rating = RateSerializer(many=True, read_only=True)
    thumbnail = serializers.CharField(source="get_first_image")
    video = serializers.CharField(source="get_first_video")
    category = serializers.CharField(source="get_category_name")

    class Meta:
        model = Course
        fields = [
            "id",
            "token_id",
            "nft_address",
            "author",
            "sellers",
            "title",
            "slug",
            "short_description",
            "keywords",
            "thumbnail",
            "video",
            "rating",
            "category",
            "price",
            "created_at",
            "updated_at",
            "compare_price",
            "discount_until",
            "discount",
            "payment",
            "language",
            "level",
            "taught",
            "best_seller",
            "status",
            "description",
        ]


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = "__all__"


class WhatLearntSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatLearnt
        fields = "__all__"


class WhoIsForSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoIsFor
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    liked_by_user = serializers.BooleanField()
    disliked_by_user = serializers.BooleanField()
    likes_count = serializers.IntegerField()
    dislikes_count = serializers.IntegerField()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class EpisodePaidSerializer(serializers.ModelSerializer):
    length = serializers.CharField(source="get_video_length_time")
    resources = ResourceSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Episode
        fields = [
            "id",
            "number",
            "title",
            "file",
            "filename",
            "date",
            "resources",
            "content",
            "description",
            "section_uuid",
            "published",
            "length",
            "comments",
        ]


class EpisodeUnPaidSerializer(serializers.ModelSerializer):
    length = serializers.CharField(source="get_video_length_time")

    class Meta:
        model = Episode
        fields = [
            "id",
            "number",
            "title",
            "date",
            "description",
            "section_uuid",
            "published",
            "length",
        ]


class SectionPaidSerializer(serializers.ModelSerializer):
    episodes = EpisodePaidSerializer(many=True)
    total_duration = serializers.CharField(source="total_length")

    class Meta:
        model = Section
        fields = [
            "id",
            "title",
            "learning_objective",
            "number",
            "episodes",
            "user",
            "published",
            "course",
            "total_duration",
        ]


class SectionUnPaidSerializer(serializers.ModelSerializer):
    episodes = EpisodeUnPaidSerializer(many=True)
    total_duration = serializers.CharField(source="total_length")

    class Meta:
        model = Section
        fields = [
            "id",
            "title",
            "learning_objective",
            "number",
            "episodes",
            "user",
            "published",
            "course",
            "total_duration",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    sellers = SellersSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = RateSerializer(many=True, read_only=True)
    images = MediaSerializer(many=True, read_only=True)
    videos = MediaSerializer(many=True, read_only=True)
    sections = SectionUnPaidSerializer(many=True, read_only=True)
    what_learnt = WhatLearntSerializer(many=True, read_only=True)
    requisites = RequisiteSerializer(many=True, read_only=True)
    who_is_for = WhoIsForSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    total_duration = serializers.CharField(source="total_course_length")
    student_rating = serializers.IntegerField(source="get_rating")
    student_rating_no = serializers.IntegerField(source="get_no_rating")
    total_lectures = serializers.IntegerField(source="get_total_lectures")

    class Meta:
        model = Course
        fields = "__all__"  # To serialize all fields


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAnalytics
        fields = "__all__"


class ViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewCount
        fields = "__all__"


class EpisodeCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeCompletion
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = "__all__"


class ViewedCoursesLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedCoursesLibrary
        fields = "__all__"


class ViewedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewed
        fields = "__all__"


class ViewedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedItem
        fields = "__all__"


class PaidCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidCoursesList
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = "__all__"
