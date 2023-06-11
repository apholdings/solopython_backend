from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "status")
    list_filter = ("author", "status")
    search_fields = ("title", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published"
    ordering = ("-published",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "author")}),
        ("Content", {"fields": ("thumbnail", "keywords", "description", "content")}),
        (
            "Additional Information",
            {"fields": ("time_read", "published", "status", "category")},
        ),
    )

    readonly_fields = ("published",)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == "published":
            return self.readonly_fields + ("status",)
        return self.readonly_fields


@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ["title", "post", "level", "order"]
    list_filter = ["level", "post__title"]
    search_fields = ["title", "post__title"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]
