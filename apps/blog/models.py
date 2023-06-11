from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from apps.category.models import Category
import uuid
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL


def blog_thumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)


# Create your models here.
class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid4)
    thumbnail = models.ImageField(
        upload_to=blog_thumbnail_directory, max_length=500, blank=True, null=True
    )

    keywords = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = RichTextField(blank=True, null=True)

    time_read = models.IntegerField(blank=True, null=True)
    featured = models.BooleanField(blank=True, null=True)

    published = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0, blank=True)

    status = models.CharField(max_length=10, choices=options, default="draft")

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return self.title

    def get_view_count(self):
        views = ViewCount.objects.filter(post=self).count()
        return views

    def get_status(self):
        status = self.status
        return status


class Heading(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="headings")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    level = models.IntegerField(
        choices=((1, "H1"), (2, "H2"), (3, "H3"), (4, "H4"), (5, "H5"), (6, "H6"))
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ViewCount(models.Model):
    post = models.ForeignKey(
        Post, related_name="blogpost_view_count", on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"
