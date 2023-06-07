from django.db import models
import uuid


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True
    )

    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=2400, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    views = models.PositiveIntegerField(default=0, blank=True)
    buyers = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.name

    def get_view_count(self):
        return self.category_view_count.count()


class ViewCount(models.Model):
    category = models.ForeignKey(
        Category, related_name="category_view_count", on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return self.ip_address
