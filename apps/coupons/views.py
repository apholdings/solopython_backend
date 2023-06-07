from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from rest_framework import status
from django.core.cache import cache
from .models import Coupon, FixedPriceCoupon, PercentageCoupon
from .serializers import CouponSerializer
from django.core.exceptions import ObjectDoesNotExist
from apps.courses.models import Course


class CheckCouponView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        coupon_name = request.query_params.get("name")
        course_id = request.query_params.get("course")

        try:
            coupon = Coupon.objects.get(name=coupon_name)

            # Check if the coupon belongs to the specified course
            if str(course_id) != str(coupon.course.id):
                return self.send_error(
                    "Coupon is not valid for this course",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if coupon.fixed_price_coupon:
                if coupon.fixed_price_coupon.uses > 0:
                    serialized_coupon = CouponSerializer(coupon).data
                    return self.send_response(
                        {
                            "coupon": serialized_coupon,
                            "type": "fixed",
                            "discount": coupon.fixed_price_coupon.discount_price,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return self.send_error(
                        "Coupon code has no uses left", status=status.HTTP_404_NOT_FOUND
                    )

            if coupon.percentage_coupon:
                if coupon.percentage_coupon.uses > 0:
                    serialized_coupon = CouponSerializer(coupon).data
                    return self.send_response(
                        {
                            "coupon": serialized_coupon,
                            "type": "percentage",
                            "discount": coupon.percentage_coupon.discount_percentage,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return self.send_error(
                        "Coupon code has no uses left", status=status.HTTP_404_NOT_FOUND
                    )
        except ObjectDoesNotExist:
            return self.send_error("Coupon not found", status=status.HTTP_404_NOT_FOUND)
