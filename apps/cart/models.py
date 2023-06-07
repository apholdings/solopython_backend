from django.db import models
from apps.courses.models import Course
from apps.coupons.models import Coupon
from djoser.signals import user_registered
import uuid
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_items = models.IntegerField(blank=True, null=True)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    referrer = models.CharField(max_length=512, blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # count = models.IntegerField(blank=True, null=True)
    # size = models.UUIDField(blank=True, null=True)
    # weight = models.UUIDField(blank=True, null=True)
    # material = models.UUIDField(blank=True, null=True)
    # color = models.UUIDField(blank=True, null=True)
    # shipping = models.UUIDField(blank=True, null=True)


def post_user_registered(request, user, *args, **kwargs):
    # 1. Definir usuario que ser registra
    user = user
    Cart.objects.create(user=user)


user_registered.connect(post_user_registered)
