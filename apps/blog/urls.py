from django.urls import path
from .views import *

urlpatterns = [
    path("posts/list/", ListPostsView.as_view()),
    path("posts/get/", DetailPostView.as_view()),
]
