from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import uuid
from django.utils import timezone
from djoser.signals import user_registered

import mercadopago
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = "Admin"
        user.verified = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    roles = (
        ("customer", "Customer"),
        ("seller", "Seller"),
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("helper", "Helper"),
        ("editor", "Editor"),
        ("owner", "Owner"),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    mercado_pago_id = models.CharField(max_length=100, blank=True, null=True)
    mercado_pago_user_id = models.CharField(max_length=100, blank=True, null=True)
    mercado_pago_merchant_id = models.CharField(max_length=100, blank=True, null=True)
    mercado_pago_client_id = models.CharField(max_length=100, blank=True, null=True)

    picture = models.ImageField(
        default="media/users/user_default_profile.png",
        upload_to="media/users/pictures/",
        blank=True,
        null=True,
        verbose_name="Picture",
    )
    banner = models.ImageField(
        default="media/users/user_default_bg.jpg",
        upload_to="media/users/pictures/",
        blank=True,
        null=True,
        verbose_name="Banner",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    is_online = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    role = models.CharField(max_length=20, choices=roles, default="customer")
    verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


def post_user_registered(request, user, *args, **kwargs):
    # 1. Definir usuario que ser registra
    user = user
    customer_data = {
        "email": user.email,
    }
    customer_response = sdk.customer().create(customer_data)
    customer = customer_response["response"]

    # Save Customer ID in Django DB
    user.mercado_pago_id = customer["id"]
    user.mercado_pago_user_id = customer["user_id"]
    user.mercado_pago_merchant_id = customer["merchant_id"]
    user.mercado_pago_client_id = customer["client_id"]
    user.save()

    # print(
    #     f"""
    #     Mercado pago Customer Created {customer}
    #     """
    # )


user_registered.connect(post_user_registered)
