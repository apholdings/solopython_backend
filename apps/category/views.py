from apps.category.serializers import CategorySerializer
from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from .models import Category, ViewCount
from slugify import slugify
from django.core.cache import cache


class PrimaryCategoriesView(StandardAPIView):
    def get(self, request, format=None):
        primary_categories = Category.objects.filter(parent=None)
        category_names = [category.name for category in primary_categories]
        return self.send_response(category_names, status=status.HTTP_200_OK)


class SubCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slugify(slug))
            sub_categories = parent_category.children.all()
            sub_category_names = [category.name for category in sub_categories]
            return self.send_response(sub_category_names, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return self.send_error(
                "Parent category does not exist.", status=status.HTTP_404_NOT_FOUND
            )


class TertiaryCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slug)
            print(parent_category)
            tertiary_categories = parent_category.children.all()
            tertiary_category_names = [
                category.name for category in tertiary_categories
            ]
            return self.send_response(
                tertiary_category_names, status=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return self.send_error(
                "Parent category does not exist.", status=status.HTTP_404_NOT_FOUND
            )


class ListPopularTopicsView(StandardAPIView):
    def get(self, request, format=None):
        cache_key = "popular_topics"
        popular_topics = cache.get(cache_key)

        if popular_topics is None:
            categories = Category.objects.order_by("views").all()[: int(6)]
            serializer = CategorySerializer(categories, many=True)
            cache.set(cache_key, serializer.data, 900)  # Cache for 15 minutes
            return self.send_response(serializer.data, status=status.HTTP_200_OK)
        else:
            return self.send_response(popular_topics, status=status.HTTP_200_OK)


class ListPrimaryCategoriesView(StandardAPIView):
    def get(self, request, format=None):
        cache_key = "primary_categories"
        primary_categories = cache.get(cache_key)

        if primary_categories is None:
            categories = Category.objects.filter(parent=None)
            serializer = CategorySerializer(categories, many=True)
            cache.set(cache_key, serializer.data, 900)  # Cache for 15 minutes
            return self.paginate_response(request, serializer.data)
        else:
            return self.paginate_response(request, primary_categories)
