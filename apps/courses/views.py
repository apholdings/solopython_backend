from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from .permissions import CanCreateCourse
from .models import *
from .serializers import *
from apps.category.models import Category
from apps.user_wallet.models import Wallet
from random import randint
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


class CreateCourseView(StandardAPIView):
    permission_classes = (CanCreateCourse,)

    def post(self, request, format=None):
        data = self.request.data
        title = data["title"]
        price = data["price"]
        category = data["category"]
        sub_category = data["sub_category"]
        topic = data["topic"]

        category = Category.objects.get(slug=category)
        sub_category = Category.objects.get(slug=sub_category)
        topic = Category.objects.get(slug=topic)

        user_wallet = Wallet.objects.get(user=request.user)

        course = Course.objects.create(
            author=request.user,
            title=title,
            price=price,
            category=category,
            sub_category=sub_category,
            topic=topic,
            token_id=random_with_N_digits(9),
        )

        sellers = Sellers.objects.create(
            author=request.user, address=user_wallet.address, course=course
        )

        course.sellers.add(sellers)

        # Create Section
        section = Section.objects.create(
            title="Introduction",
            learning_objective="Enter a learning objective",
            number=1,
            published=False,
            user=request.user,
            course=course,
        )

        course.sections.add(section)

        episode = Episode.objects.create(
            title="Introduction",
            number=1,
            published=False,
            content="",
            description="",
            user=request.user,
            course=course,
            section_uuid=section.id,
        )

        section.episodes.add(episode)

        return self.send_response(
            "Course Created Successfully", status=status.HTTP_201_CREATED
        )


class ListCoursesAuthorView(StandardAPIView):
    permission_classes = (CanCreateCourse,)

    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(author=request.user)
        serializer = CourseListSerializer(courses, many=True)
        return self.paginate_response(request, serializer.data)


class ListCoursesView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()

        # filtros de categoría
        categories = self.request.query_params.getlist("category", [])
        # sub_categories = self.request.query_params.getlist('sub_category', [])
        # topics = self.request.query_params.getlist('topic', [])

        # otros filtros
        sorting = self.request.query_params.get("sorting", None)
        prices = self.request.query_params.getlist("price", [])
        languages = self.request.query_params.getlist("language", [])
        levels = self.request.query_params.getlist("level", [])

        print(
            f"""
                Categories: {categories}
                Prices: {prices}
                Languages: {languages}
                Levels: {levels}
                Sorting: {sorting}
              """
        )

        if categories:
            courses = courses.filter(category__id__in=categories)

        # if sub_categories:
        #     courses = courses.filter(sub_category__name__in=sub_categories)

        # if topics:
        #     courses = courses.filter(topic__name__in=topics)

        if prices:
            query = Q()
            for price in prices:
                min_price, max_price = price.split("-")
                if max_price == "":
                    query |= Q(price__gte=min_price)
                else:
                    query |= Q(price__gte=min_price, price__lte=max_price)
            courses = courses.filter(query)

        if languages:
            courses = courses.filter(language__in=languages)

        if levels:
            courses = courses.filter(level__in=levels)

        if sorting:
            if sorting == "sold":
                courses = courses.order_by("-sold")
            elif sorting == "students":
                courses = courses.order_by("-students")
            elif sorting == "views":
                courses = courses.order_by("-views")
            elif sorting == "student_rating":
                courses = courses.order_by("-student_rating")
            elif sorting == "created_at":
                courses = courses.order_by("-created_at")

        serializer = CourseListSerializer(courses, many=True)
        return self.paginate_response(request, serializer.data)


class DetailCourseView(StandardAPIView):
    def get(self, request, slug, *args, **kwargs):
        course = Course.objects.get(slug=slug)
        serializer = CourseDetailSerializer(course)
        return self.send_response(serializer.data)


class ListPaidCoursesView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        paid_courses_list = PaidCoursesList.objects.get(user=user)
        courses = paid_courses_list.courses

        # filtros de categoría
        categories = self.request.query_params.getlist("category", [])
        # sub_categories = self.request.query_params.getlist('sub_category', [])
        # topics = self.request.query_params.getlist('topic', [])

        # otros filtros
        sorting = self.request.query_params.get("sorting", None)
        prices = self.request.query_params.getlist("price", [])
        languages = self.request.query_params.getlist("language", [])
        levels = self.request.query_params.getlist("level", [])

        print(
            f"""
                Categories: {categories}
                Prices: {prices}
                Languages: {languages}
                Levels: {levels}
                Sorting: {sorting}
              """
        )

        if categories:
            courses = courses.filter(category__id__in=categories)

        # if sub_categories:
        #     courses = courses.filter(sub_category__name__in=sub_categories)

        # if topics:
        #     courses = courses.filter(topic__name__in=topics)

        if prices:
            query = Q()
            for price in prices:
                min_price, max_price = price.split("-")
                if max_price == "":
                    query |= Q(price__gte=min_price)
                else:
                    query |= Q(price__gte=min_price, price__lte=max_price)
            courses = courses.filter(query)

        if languages:
            courses = courses.filter(language__in=languages)

        if levels:
            courses = courses.filter(level__in=levels)

        if sorting:
            if sorting == "sold":
                courses = courses.order_by("-sold")
            elif sorting == "students":
                courses = courses.order_by("-students")
            elif sorting == "views":
                courses = courses.order_by("-views")
            elif sorting == "student_rating":
                courses = courses.order_by("-student_rating")
            elif sorting == "created_at":
                courses = courses.order_by("-created_at")

        serializer = CourseListSerializer(courses, many=True)
        return self.paginate_response(request, serializer.data)


class ListPaidSectionsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug, *args, **kwargs):
        user = request.user
        course = Course.objects.get(slug=slug)
        user_paid_courses = PaidCoursesList.objects.get(user=user)
        if course in user_paid_courses.courses.all():  # Call .all() here
            sections = (
                course.sections.all()
            )  # Also call .all() here if sections is a related field
            print(sections)
            serializer = SectionPaidSerializer(sections, many=True)
            return self.paginate_response(request, serializer.data)
        else:
            return self.send_error("Course not in paid list")


class CreateCommentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        episode = Episode.objects.get(id=request.data["episode_id"])
        comment = Comment.objects.create(
            user=user, body=request.data["content"], episode=episode
        )
        episode.comments.add(comment)

        episode_comments = episode.comments.all()
        serializer = CommentSerializer(episode_comments, many=True).data
        return self.paginate_response(request, serializer)


class ListCommentsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        episode_id = self.request.query_params.get("episode")
        episode = Episode.objects.get(id=episode_id)
        episode_comments = episode.comments.all()
        serializer = CommentSerializer(episode_comments, many=True).data
        return self.paginate_response(request, serializer)


class EditCommentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        comment = Comment.objects.get(user=request.user, id=request.data["comment_id"])
        comment.body = request.data["content"]  # Update the comment's body
        comment.save()  # Save the updated comment
        episode = comment.episode  # Retrieve the episode associated with the comment
        episode_comments = episode.comments.all()
        serializer = CommentSerializer(episode_comments, many=True).data
        return self.paginate_response(request, serializer)


class DeleteCommentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, comment_id, format=None):
        try:
            comment = Comment.objects.get(id=comment_id)
            episode = (
                comment.episode
            )  # Retrieve the episode associated with the comment
        except Comment.DoesNotExist:
            return self.send_error("Comment not found.", status=404)

        if comment.user != request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")

        comment.delete()

        episode_comments = episode.comments.all()
        serializer = CommentSerializer(episode_comments, many=True).data

        return self.paginate_response(request, serializer)
