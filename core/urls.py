from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path("api/users/wallet/", include("apps.user_wallet.urls")),
    path("api/category/", include("apps.category.urls")),
    path("api/courses/", include("apps.courses.urls")),
    path("api/coupons/", include("apps.coupons.urls")),
    path("api/cart/", include("apps.cart.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/reviews/", include("apps.reviews.urls")),
    path("api/tiers/", include("apps.tiers.urls")),
    path("api/contacts/", include("apps.contacts.urls")),
    path("api/blog/", include("apps.blog.urls")),
    path("api/newsletter/", include("apps.newsletter.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
