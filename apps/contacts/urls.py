from django.urls import path
from .views import *

urlpatterns = [path("create/", ContactCreateView.as_view())]
