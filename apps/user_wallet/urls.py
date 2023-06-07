from django.urls import path

from .views import *


urlpatterns = [
    path("me/", MyUserWalletView.as_view()),
    # path('<post_slug>', PostDetailView.as_view()),
    # path("search/<str:search_term>",SearchBlogView.as_view()),
]
