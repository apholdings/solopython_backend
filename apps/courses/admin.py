from django.contrib import admin
from .models import *


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["id", "position_id", "title", "file", "media_type", "course"]
    list_filter = ["media_type"]
    search_fields = ["title"]


@admin.register(Sellers)
class SellersAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "address"]
    list_filter = ["author"]
    search_fields = ["address"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "token_id",
        "nft_address",
        "author",
        "title",
        "slug",
        "short_description",
        "description",
        "keywords",
        "category",
        "sub_category",
        "topic",
        "created_at",
        "updated_at",
        "student_rating",
        "stock",
        "price",
        "compare_price",
        "discount_until",
        "discount",
        "payment",
        "language",
        "level",
        "taught",
        "welcome_message",
        "congrats_message",
        "sold",
        "course_length",
        "students",
        "views",
        "best_seller",
        "status",
    ]
    list_filter = ["author", "category", "status", "payment", "language", "level"]
    search_fields = ["title", "description", "keywords"]
    date_hierarchy = "created_at"


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "views",
        "clicks",
        "impressions",
        "clickThroughRate",
        "purchases",
        "conversion_rate",
        "avg_time_on_page",
        "sold",
        "income_earned",
    ]
    list_filter = ["course"]


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ["course", "ip_address"]
    list_filter = ["course"]


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ["rate_number", "user", "course"]
    list_filter = ["rate_number", "user", "course"]
    search_fields = ["user__username"]


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    list_display = ["id", "position_id", "title", "user", "course"]
    list_filter = ["user", "course"]
    search_fields = ["title", "user__username"]


@admin.register(WhatLearnt)
class WhatLearntAdmin(admin.ModelAdmin):
    list_display = ["id", "position_id", "title", "user", "course"]
    list_filter = ["user", "course"]
    search_fields = ["title", "user__username"]


@admin.register(WhoIsFor)
class WhoIsForAdmin(admin.ModelAdmin):
    list_display = ["id", "position_id", "title", "user", "course"]
    list_filter = ["user", "course"]
    search_fields = ["title", "user__username"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "number", "user", "published", "course"]
    list_filter = ["user", "published", "course"]
    search_fields = ["title", "user__username"]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "number", "user", "course", "published"]
    list_filter = ["user", "course", "published"]
    search_fields = ["title", "user__username"]


@admin.register(EpisodeCompletion)
class EpisodeCompletionAdmin(admin.ModelAdmin):
    list_display = ["user", "episode", "course", "completed"]
    list_filter = ["user", "episode", "course", "completed"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user"]
    list_filter = ["user"]
    search_fields = ["title", "user__username"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "title",
        "created_date",
        "episode",
        "has_accepted_answer",
    ]
    list_filter = ["user", "created_date", "episode", "has_accepted_answer"]
    search_fields = ["title", "user__username", "body"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "question", "created_date", "is_accepted_answer"]
    list_filter = ["user", "question", "created_date", "is_accepted_answer"]
    search_fields = ["body", "user__username"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_filter = ["user"]


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_filter = ["user"]


@admin.register(ViewedCoursesLibrary)
class ViewedCoursesLibraryAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(Viewed)
class ViewedAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "date_created"]
    list_filter = ["user", "date_created"]


@admin.register(ViewedItem)
class ViewedItemAdmin(admin.ModelAdmin):
    list_display = ["id", "library", "course", "date_created"]
    list_filter = ["library", "course", "date_created"]


@admin.register(PaidCoursesList)
class PaidAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_filter = ["user", "created_at"]


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_items", "date_created"]
    list_filter = ["user", "date_created"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "episode", "body", "created_at"]
    list_filter = ["user", "created_at"]
