from django.urls import path
from .views import *

urlpatterns = [
    path("create/", CreateCourseView.as_view()),
    path("list/author/", ListCoursesAuthorView.as_view()),
    path("list/", ListCoursesView.as_view()),
    path("list_paid/", ListPaidCoursesView.as_view()),
    path("sections/<slug>/paid/list/", ListPaidSectionsView.as_view()),
    path("get/<slug>/", DetailCourseView.as_view()),
    path("episode/comment/create/", CreateCommentView.as_view()),
    path("episode/comment/edit/", EditCommentView.as_view()),
    path("episode/comment/list/", ListCommentsView.as_view()),
    path("episode/comment/delete/<comment_id>/", DeleteCommentView.as_view()),
]
