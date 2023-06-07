from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "birthday")
    search_fields = ("user__username", "location")
    list_filter = ("location",)


admin.site.register(Profile, ProfileAdmin)
