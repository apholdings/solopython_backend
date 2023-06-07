from django.contrib import admin
from .models import FriendRequest, FriendList


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "timestamp", "is_archived", "is_accepted")
    search_fields = ("from_user__username", "to_user__username")
    list_filter = ("is_archived", "is_accepted")


class FriendListAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(FriendList, FriendListAdmin)
