from django.urls import path
from .views import *

urlpatterns = [
    path("create/", CreateCourseView.as_view()),
    path("list/author/", ListCoursesAuthorView.as_view()),
    path("list/", ListCoursesView.as_view()),
    path("list/by_category/", ListCoursesByCategoryView.as_view()),
    path("list_paid/", ListPaidCoursesView.as_view()),
    path("sections/<slug>/paid/list/", ListPaidSectionsView.as_view()),
    path("get/<slug>/", DetailCourseView.as_view()),
    path("episode/comment/create/", CreateCommentView.as_view()),
    path("episode/comment/edit/", EditCommentView.as_view()),
    path("episode/comment/list/", ListCommentsView.as_view()),
    path("episode/comment/delete/<comment_id>/", DeleteCommentView.as_view()),
    path("episode/questions/list/", ListQuestionsView.as_view()),
    path("episode/questions/create/", CreateQuestionView.as_view()),
    path("episode/questions/edit/", EditQuestionView.as_view()),
    path("episode/questions/delete/<question_id>/", DeleteQuestionView.as_view()),
    path("episode/questions/like/", QuestionLikeView.as_view()),
    path("episode/questions/answers/list/", ListAnswersView.as_view()),
    path("episode/questions/answers/create/", CreateAnswerView.as_view()),
    path("episode/questions/answers/edit/", EditAnswerView.as_view()),
    path("episode/questions/answers/delete/<answer_id>/", DeleteAnswerView.as_view()),
    path("episode/questions/answers/like/", AnswerLikeView.as_view()),
    path("episode/questions/answers/accept/", AcceptAnswerView.as_view()),
]
