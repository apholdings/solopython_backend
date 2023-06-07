from django.db import models
from django.conf import settings
from djoser.signals import user_registered
from asgiref.sync import async_to_sync
from apps.user_profile.models import Profile
from django.core.exceptions import ObjectDoesNotExist


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friend_requests_sent",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friend_requests_received",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("from_user", "to_user")


class FriendList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend_list"
    )
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="friends"
    )

    def __str__(self):
        return self.user.username


def post_user_registered(request, user, *args, **kwargs):
    # 1. Definir usuario que ser registra
    user = user
    FriendList.objects.create(user=user)


user_registered.connect(post_user_registered)
