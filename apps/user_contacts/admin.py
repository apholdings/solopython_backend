from django.contrib import admin
from .models import (
    SellerContact,
    InstructorContact,
    FriendContact,
    SellerContactList,
    InstructorContactList,
    FriendContactList,
)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "contact", "date_created")
    search_fields = ("user__username", "contact__username")


class ContactListAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


admin.site.register(SellerContact, ContactAdmin)
admin.site.register(InstructorContact, ContactAdmin)
admin.site.register(FriendContact, ContactAdmin)

admin.site.register(SellerContactList, ContactListAdmin)
admin.site.register(InstructorContactList, ContactListAdmin)
admin.site.register(FriendContactList, ContactListAdmin)
