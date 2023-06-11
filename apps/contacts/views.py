from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from rest_framework import status
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class ContactCreateView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        # serializer = ContactSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # contact = serializer.save()

        # # Render the HTML email template
        # email_context = {
        #     "name": contact.name,
        #     "email": contact.email,
        #     "message": contact.message,
        #     "budget": contact.budget,
        #     "telephone": contact.telephone,
        # }
        # html_message = render_to_string("email/contact.html", email_context)

        # # Send the HTML email
        # send_mail(
        #     "SoloPython Contact Form Prospect",
        #     strip_tags(html_message),  # Strip HTML tags for the plain text version
        #     "mail@solopython.com",
        #     ["mail@solopython.com"],
        #     fail_silently=False,
        #     html_message=html_message,
        # )

        return self.send_response("Message sent successfully")
