from django.urls import path
from .views import *


urlpatterns = [path("signup/", NewsletterSignupView.as_view())]
