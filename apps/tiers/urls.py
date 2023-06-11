from django.urls import path

from .views import *

urlpatterns = [
    path("create/", CreateTierView.as_view()),
    path("list/", ListTiersView.as_view()),
    path("get/", DetailTierView.as_view()),
    path("user_subscriptions/", ListUserSubscriptionsView.as_view()),
    path("subscriptions/update", UpdateSubscritionView.as_view()),
]
