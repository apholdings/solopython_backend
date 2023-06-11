from djoser.serializers import PasswordResetConfirmSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "picture",
            "banner",
            "first_name",
            "last_name",
            "is_online",
            "is_active",
            "is_staff",
            "role",
            "verified",
            "date_joined",
            "updated_at",
        ]


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def build_password_reset_confirm_url(self, uid, token):
        url = f"?forgot_password_confirm=True&uid={uid}&token={token}"
        return url
