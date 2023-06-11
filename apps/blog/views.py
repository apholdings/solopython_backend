from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from .serializers import PostSerializer, HeadingSerializer
from .models import *
from django.db.models.query_utils import Q


class ListPostsView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.filter(status="published")

            search_term = request.query_params.get("search")
            if search_term and search_term != "none":
                posts = posts.filter(
                    Q(title__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(content__icontains=search_term)
                    | Q(category__name__icontains=search_term)
                )

            category_slug = request.query_params.get("category")
            if category_slug and category_slug != "none":
                category = Category.objects.get(slug=category_slug)
                # Filtrar categoria sola si es que no tiene children
                if not Category.objects.filter(parent=category).exists():
                    posts = posts.filter(category=category)
                else:
                    categories = []
                    if category.parent:
                        # Filter posts by parent category
                        parent_category = category.parent
                        categories.append(parent_category)

                    # Filtrar categoria si es que tiene children
                    child_categories = Category.objects.filter(parent=category)
                    for child_category in child_categories:
                        # Get children categories of the child category
                        children_categories = Category.objects.filter(
                            parent=child_category
                        )
                        categories.extend(children_categories)

                    # Filter posts by categories list
                    posts = posts.filter(category__in=categories)

            serializer = PostSerializer(posts, many=True).data
            return self.paginate_response(request, serializer)

        except Category.DoesNotExist:
            return self.send_error(
                "Invalid category slug", status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return self.send_error(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailPostView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        try:
            slug = request.query_params.get("slug")
            post = Post.objects.get(slug=slug)
            headings = post.headings.all()
            heading_serializer = HeadingSerializer(headings, many=True).data
            serializer = PostSerializer(post).data

            response_data = {"headings": heading_serializer, "post": serializer}

            address = request.META.get("HTTP_X_FORWARDED_FOR")
            if address:
                ip = address.split(",")[-1].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")

            if not ViewCount.objects.filter(post=post, ip_address=ip).exists():
                view = ViewCount(post=post, ip_address=ip)
                view.save()
                post.views += 1
                post.save()

            return self.send_response(response_data)

        except Post.DoesNotExist:
            return self.send_error("Invalid post ID", status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return self.send_error(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
