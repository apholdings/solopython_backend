from django.contrib import admin
from .models import Newsletter, NewsletterUser


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created")
    search_fields = ("name", "subject")
    date_hierarchy = "created"
    filter_horizontal = ("email",)


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display = ("email", "date_added")
    search_fields = ("email",)
    date_hierarchy = "date_added"


admin.site.site_header = "Newsletter Admin"
admin.site.site_title = "Newsletter Admin"
