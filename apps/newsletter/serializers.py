from rest_framework import serializers
from .models import NewsletterUser, Newsletter


class NewsletterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterUser
        fields = ["id", "email", "date_added"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "name", "subject", "body", "email", "created"]
