from django.contrib import admin

# Register your models here.
from .models import *


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "title",
        "views",
        "buyers",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_filter = (
        "name",
        "views",
        "buyers",
    )
    list_editable = (
        "title",
        "views",
        "buyers",
    )
    search_fields = (
        "name",
        "title",
        "description",
        "views",
        "buyers",
    )
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25


admin.site.register(Category, CourseAdmin)
