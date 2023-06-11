from django.db import models
from datetime import datetime
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    budget = models.IntegerField()
    phone = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
