from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from apps.courses.models import Course, Rate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.user.serializers import UserSerializer
from rest_framework.response import Response


class ListCourseReviewsView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        # Get the course using the identifier (UUID, slug, or nft_address)
        course_id = self.request.query_params.get("course_id")
        course = Course.objects.get(id=course_id)
        rating_filter = request.GET.get("rating", None)

        if rating_filter is not None and rating_filter != "undefined":
            reviews = Review.objects.filter(course=course, rating=rating_filter)
        else:
            reviews = Review.objects.filter(course=course)

        review_counts = []
        total_rating = 0
        for rating in range(1, 6):
            count = reviews.filter(rating=rating).count()
            total_rating += rating * count
            review_counts.append({"rating": rating, "count": count})

        review_average = (
            float(total_rating) / float(reviews.count()) if reviews.count() > 0 else 0
        )

        review_data = {
            "totalCount": reviews.count(),
            "counts": review_counts,
            "average": review_average,
        }

        return self.paginate_response_with_extra(
            request, ReviewSerializer(reviews, many=True).data, review_data
        )


class GetCourseReviewView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id, format=None):
        user = request.user
        course = Course.objects.get(id=id)
        try:
            review = Review.objects.get(user=user, course=course)
            return self.send_response(ReviewSerializer(review).data)
        except ObjectDoesNotExist:
            return self.send_response(False)


class CreateReviewView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        data = self.request.data

        course_uuid = data["course_id"]

        try:
            rating = float(data["rating"])
        except:
            return self.send_error("Rating must be a decimal value")
        try:
            comment = str(data["content"])
        except:
            return self.send_error("Must pass a comment when creating review")

        if not Course.objects.filter(id=course_uuid).exists():
            return self.send_error("Course does not exist")

        course = Course.objects.get(id=course_uuid)

        if Review.objects.filter(user=user, course=course).exists():
            return self.send_error("Review for this course already created")

        review = Review(user=user, course=course, rating=rating, comment=comment)
        review.save()

        rate = Rate.objects.create(rate_number=rating, user=user)
        course.rating.add(rate)

        ratings = course.rating.all()
        rate = 0
        for rating in ratings:
            rate += rating.rate_number
        try:
            rate /= len(ratings)
        except ZeroDivisionError:
            rate = 0

        course.student_rating = rate
        course.save()

        return self.send_response(ReviewSerializer(review).data)


class UpdateCourseReviewView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        data = self.request.data
        user = self.request.user

        course_id = data["course_id"]

        try:
            rating = float(data["review_rating"])
        except:
            return self.send_error("Rating must be a decimal value")
        try:
            comment = str(data["reviewBody"])
        except:
            return self.send_error("Must pass a comment when creating review")
        try:
            review_id = str(data["review_id"])
        except:
            return self.send_error("Must pass a comment when creating review")

        review = Review.objects.get(id=review_id)

        review.rating = rating
        review.comment = comment
        review.save()

        course = Course.objects.get(id=course_id)

        ratings = course.rating.all()
        rate = 0
        for rating in ratings:
            rate += rating.rate_number
        try:
            rate /= len(ratings)
        except ZeroDivisionError:
            rate = 0

        course.student_rating = rate
        course.save()

        rating = course.rating.all()

        result = {}
        results = []
        rating_list = []
        star_list_1 = []
        star_list_2 = []
        star_list_3 = []
        star_list_4 = []
        star_list_5 = []

        def Average(lst):
            return sum(lst) / len(lst)

        if Review.objects.filter(user=user, course=course).exists():
            result = ReviewSerializer(review).data
            result["verified"] = review.user.verified
            result["thumbnail"] = review.user.picture.url

            reviews = Review.objects.order_by("-date_created").filter(course=course)

            for review in reviews:
                item = {}
                user_data = UserSerializer(
                    review.user
                ).data  # Serialize the user object

                item["id"] = review.id
                item["rating"] = review.rating
                item["comment"] = review.comment
                item["date_created"] = review.date_created
                item["user"] = user_data
                item["verified"] = review.user.verified
                item["thumbnail"] = review.user.picture.url

                if review.rating == 1:
                    star_list_1.append(review.rating)
                if review.rating == 2:
                    star_list_2.append(review.rating)
                if review.rating == 3:
                    star_list_3.append(review.rating)
                if review.rating == 4:
                    star_list_4.append(review.rating)
                if review.rating == 5:
                    star_list_5.append(review.rating)

                results.append(item)
                rating_list.append(review.rating)
            average = Average(rating_list)

        review_counts = []
        total_rating = 0
        for rating in range(1, 6):
            count = reviews.filter(rating=rating).count()
            total_rating += rating * count
            review_counts.append({"rating": rating, "count": count})

        extra_data = {
            "review": result,
            "average_rating": average,
            "totalCount": reviews.count(),
            "counts": review_counts,
        }

        return self.paginate_response_with_extra(request, results, extra_data)


class DeleteCourseReviewView(StandardAPIView):
    def delete(self, request, course_uuid, format=None):
        data = self.request.data
        user = self.request.user

        try:
            if not Course.objects.filter(course_uuid=course_uuid).exists():
                return self.send_error(
                    "This course does not exist", status=status.HTTP_404_NOT_FOUND
                )

            course = Course.objects.get(course_uuid=course_uuid)

            results = []

            if Review.objects.filter(user=user, course=course).exists():
                Review.objects.filter(user=user, course=course).delete()

                reviews = Review.objects.order_by("-date_created").filter(course=course)

                for review in reviews:
                    item = {}

                    item["id"] = review.id
                    item["rating"] = review.rating
                    item["comment"] = review.comment
                    item["date_created"] = review.date_created
                    item["user"] = review.user.first_name

                    results.append(item)

                return self.paginate_response(results, status=status.HTTP_200_OK)
            else:
                return self.send_error(
                    {"error": "Review for this product does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except:
            return self.send_error(
                {"error": "Something went wrong when deleting product review"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FilterCourseReviewsView(StandardAPIView):
    def get(self, request, course_uuid, format=None):
        if not Course.objects.filter(course_uuid=course_uuid).exists():
            return self.send_error(
                "This course does not exist", status=status.HTTP_404_NOT_FOUND
            )

        course = Course.objects.get(course_uuid=course_uuid)

        rating = request.query_params.get("rating")

        try:
            rating = float(rating)
        except:
            return self.send_error(
                "Rating must be a decimal value", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if not rating:
                rating = 5.0
            elif rating > 5.0:
                rating = 5.0
            elif rating < 0.5:
                rating = 0.5

            results = []

            if Review.objects.filter(course=course).exists():
                if rating == 0.5:
                    reviews = Review.objects.order_by("-date_created").filter(
                        rating=rating, course=course
                    )
                else:
                    reviews = (
                        Review.objects.order_by("-date_created")
                        .filter(rating__lte=rating, course=course)
                        .filter(rating__gte=(rating - 0.5), course=course)
                    )

                serializer = ReviewSerializer(reviews, many=True)

                results_length = len(reviews)

            return self.paginate_response_with_extra(
                request, {"reviews": serializer.data, "length": results_length}
            )
        except:
            return self.send_error(
                "Something went wrong when filtering reviews for product",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
