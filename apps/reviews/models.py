from apps.courses.models import Course
from django.db import models
from django.utils.timezone import now
from django.conf import settings

User = settings.AUTH_USER_MODEL
import uuid

# from apps.classroom.models import CourseClassRoom
# Create your models here.


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
