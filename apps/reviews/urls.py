from django.urls import path
from .views import *

app_name = "reviews"

urlpatterns = [
    path("course/list/", ListCourseReviewsView.as_view()),
    path("course/create/", CreateReviewView.as_view()),
    path("course/edit/", UpdateCourseReviewView.as_view()),
    path("course/get/<id>/", GetCourseReviewView.as_view()),
]
