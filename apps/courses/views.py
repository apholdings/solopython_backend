from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from .permissions import CanCreateCourse
from .models import *
from .serializers import *
from apps.category.models import Category
from apps.user_wallet.models import Wallet
from random import randint
from django.db.models import Q, F
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

        search = request.query_params.get("search", None)
        if search and "null" not in search:
            courses = Course.objects.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(short_description__icontains=search)
                | Q(keywords__icontains=search)
                | Q(category__name__icontains=search)
                | Q(category__title__icontains=search)
                | Q(category__description__icontains=search)
            )

        # filtros de categoría
        categories = self.request.query_params.getlist("category", [])
        if categories:
            courses = courses.filter(category__slug__in=categories)
        # sub_categories = self.request.query_params.getlist('sub_category', [])
        # topics = self.request.query_params.getlist('topic', [])

        # otros filtros
        sorting = self.request.query_params.get("sorting", None)
        prices = self.request.query_params.getlist("price", [])
        languages = self.request.query_params.getlist("language", [])
        levels = self.request.query_params.getlist("level", [])

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


class ListCoursesByCategoryView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        categories = self.request.query_params.getlist("category", [])
        courses = Course.objects.filter(category__slug__in=categories)

        search = request.query_params.get("search", None)
        if search and "null" not in search:
            courses = Course.objects.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(short_description__icontains=search)
                | Q(keywords__icontains=search)
                | Q(category__name__icontains=search)
                | Q(category__title__icontains=search)
                | Q(category__description__icontains=search)
            )

        # otros filtros
        sorting = self.request.query_params.get("sorting", None)
        prices = self.request.query_params.getlist("price", [])
        languages = self.request.query_params.getlist("language", [])
        levels = self.request.query_params.getlist("level", [])

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

        search = request.query_params.get("search", None)
        if search and "null" not in search:
            courses = Course.objects.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(short_description__icontains=search)
                | Q(keywords__icontains=search)
                | Q(category__name__icontains=search)
                | Q(category__title__icontains=search)
                | Q(category__description__icontains=search)
            )

        # otros filtros
        sorting = self.request.query_params.get("sorting", None)
        prices = self.request.query_params.getlist("price", [])
        languages = self.request.query_params.getlist("language", [])
        levels = self.request.query_params.getlist("level", [])

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


class ListQuestionsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        episode_id = self.request.query_params.get("episode")
        episode = Episode.objects.get(id=episode_id)
        questions = episode.questions.all()

        order_by = self.request.query_params.get("order_by")
        if order_by is not "":
            print("Order by")

        filter_by = self.request.query_params.get("filter_by")
        if filter_by is not "":
            print("filter by")

        search_by = self.request.query_params.get("search")
        if search_by != "":
            query = Q(title__icontains=search_by) | Q(body__icontains=search_by)
            questions = questions.filter(query)

        serializer = QuestionSerializer(questions, many=True).data
        return self.paginate_response(request, serializer)


class CreateQuestionView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        episode = Episode.objects.get(id=request.data["episode_id"])
        question = Question.objects.create(
            user=user,
            title=request.data["title"],
            body=request.data["content"],
            episode=episode,
        )
        episode.questions.add(question)

        episode_questions = episode.questions.all()
        serializer = QuestionSerializer(episode_questions, many=True).data
        return self.paginate_response(request, serializer)


class EditQuestionView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        question = Question.objects.get(
            user=request.user, id=request.data["question_id"]
        )
        question.title = request.data["title"]  # Update the comment's body
        question.body = request.data["content"]  # Update the comment's body
        question.save()  # Save the updated comment
        episode = question.episode  # Retrieve the episode associated with the comment
        episode_questions = episode.questions.all()
        serializer = CommentSerializer(episode_questions, many=True).data
        return self.paginate_response(request, serializer)


class DeleteQuestionView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, question_id, format=None):
        try:
            question = Question.objects.get(id=question_id)
            episode = (
                question.episode
            )  # Retrieve the episode associated with the comment
        except Question.DoesNotExist:
            return self.send_error("Question not found.", status=404)

        if question.user != request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")

        question.delete()

        episode_questions = episode.questions.all()
        serializer = QuestionSerializer(episode_questions, many=True).data

        return self.paginate_response(request, serializer)


class QuestionLikeView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = request.user

        question_id = request.data["question_id"]
        question = Question.objects.get(id=question_id)

        liked_item = None
        for like in question.likes.all():
            if like.user == user:
                liked_item = like
                break

        if liked_item is None:
            new_like = Like.objects.create(user=user)
            question.likes.add(new_like)
        else:
            question.likes.remove(liked_item)
            liked_item.delete()  # Delete the Like object

        # Update like counter
        question.likes_count = (
            F("likes_count") + 1 if liked_item is None else F("likes_count") - 1
        )
        question.save()

        return self.send_response("Question liked")


class ListAnswersView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        question_id = self.request.query_params.get("question")
        question = Question.objects.get(id=question_id)
        answers = question.answers.all()

        search_by = self.request.query_params.get("search")
        if search_by != "":
            query = Q(title__icontains=search_by) | Q(body__icontains=search_by)
            answers = answers.filter(query)

        serializer = AnswerSerializer(answers, many=True).data
        return self.paginate_response(request, serializer)


class CreateAnswerView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        question = Question.objects.get(id=request.data["question_id"])
        answer = Answer.objects.create(
            user=user,
            body=request.data["content"],
            question=question,
        )
        question.answers.add(answer)

        question_answers = question.answers.all()
        serializer = AnswerSerializer(question_answers, many=True).data
        return self.paginate_response(request, serializer)


class EditAnswerView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        answer = Answer.objects.get(user=request.user, id=request.data["answer_id"])
        answer.body = request.data["content"]  # Update the answer's body
        answer.save()  # Save the updated answer
        question = answer.question  # Retrieve the question associated with the answer
        question_answers = question.answers.all()
        serializer = AnswerSerializer(question_answers, many=True).data
        return self.paginate_response(request, serializer)


class DeleteAnswerView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, answer_id, format=None):
        try:
            answer = Answer.objects.get(id=answer_id)
            question = (
                answer.question
            )  # Retrieve the episode associated with the comment
        except Answer.DoesNotExist:
            return self.send_error("Answer not found.", status=404)

        if answer.user != request.user:
            raise PermissionDenied("You do not have permission to delete this answer.")

        answer.delete()

        question_answers = question.answers.all()
        serializer = AnswerSerializer(question_answers, many=True).data

        return self.paginate_response(request, serializer)


class AnswerLikeView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = request.user

        answer_id = request.data["answer_id"]
        answer = Answer.objects.get(id=answer_id)

        liked_item = None
        for like in answer.likes.all():
            if like.user == user:
                liked_item = like
                break

        if liked_item is None:
            new_like = Like.objects.create(user=user)
            answer.likes.add(new_like)
        else:
            answer.likes.remove(liked_item)
            liked_item.delete()  # Delete the Like object

        # Update like counter
        answer.likes_count = (
            F("likes_count") + 1 if liked_item is None else F("likes_count") - 1
        )
        answer.save()

        return self.send_response("Answer liked")


class AcceptAnswerView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = request.user
        try:
            answer = Answer.objects.get(id=request.data["answer_id"])
        except Answer.DoesNotExist:
            return self.send_error(
                "Answer does not exist.", status=status.HTTP_404_NOT_FOUND
            )

        question = answer.question  # Get the related question from the answer object

        if question.user == user:
            if answer.is_accepted_answer:
                answer.is_accepted_answer = False
                question.has_accepted_answer = False
                question.correct_answer = None
            else:
                answer.is_accepted_answer = True
                question.has_accepted_answer = True
                question.correct_answer = answer
            answer.save()  # Save the updated answer object
            question.save()  # Save the updated question object

            return self.send_response("Success", status=status.HTTP_200_OK)
        else:
            return self.send_error(
                "User not allowed.", status=status.HTTP_403_FORBIDDEN
            )
