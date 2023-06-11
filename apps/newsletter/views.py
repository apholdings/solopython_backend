from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import APIException
from .models import *
from .serializers import *


class DuplicateEmailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Email address already exists."
    default_code = "duplicate_email"


class NewsletterSignupView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.data.get("email")

        if NewsletterUser.objects.filter(email=email).exists():
            raise DuplicateEmailException()

        newsletter_user = NewsletterUser(email=email)
        newsletter_user.save()

        return self.send_response("Successfully added user.")
