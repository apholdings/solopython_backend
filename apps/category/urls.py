from django.urls import path
from .views import *

urlpatterns = [
    path("list/primary/", PrimaryCategoriesView.as_view()),
    path("list/secondary/<slug>/", SubCategoriesView.as_view()),
    path("list/tertiary/<str:slug>/", TertiaryCategoriesView.as_view()),
    path("list/popular/", ListPopularTopicsView.as_view()),
    path("list/parent/", ListPrimaryCategoriesView.as_view()),
]
