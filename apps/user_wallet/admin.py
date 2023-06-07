from django.contrib import admin
from .models import Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "address")
    search_fields = ("user__username", "address")
    readonly_fields = (
        "address",
        "user",
    )
    exclude = ("private_key",)


admin.site.register(Wallet, WalletAdmin)
