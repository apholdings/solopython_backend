from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
import mercadopago
from django.conf import settings
from apps.coupons.models import Coupon
from apps.courses.models import PaidCoursesList, Course
from apps.cart.models import Cart

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


class CreditCardPaymentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user

        data = request.data
        cart = data["cart"]

        token = data["token"]
        issuer_id = data["issuer_id"]
        payment_method_id = data["payment_method_id"]
        transaction_amount = data["transaction_amount"]
        installments = data["installments"]
        payer = data["payer"]
        email = payer.get("email")
        identification_type = payer.get("identification").get("type")
        identification_number = payer.get("identification").get("number")

        # Create Payment Data Dictionary
        payment_data = {
            "transaction_amount": float(transaction_amount),
            "token": token,
            "installments": int(installments),
            "payment_method_id": payment_method_id,
            "issuer_id": issuer_id,
            "payer": {
                "email": email,
                "identification": {
                    "type": identification_type,
                    "number": identification_number,
                },
            },
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        if payment["status"] == "approved":
            # Crear Modelo de Transaccion
            for cart_item in cart:
                if cart_item.get("coupon") is not None:
                    # handle coupon
                    coupon_id = cart_item["coupon"]["id"]
                    coupon = Coupon.objects.get(id=coupon_id)
                    # Reduce uses
                    if coupon.fixed_price_coupon:
                        coupon.fixed_price_coupon.uses -= 1
                    if coupon.percentage_coupon:
                        coupon.percentage_coupon.uses -= 1
                    coupon.save()

                if cart_item.get("course") is not None:
                    # handle course
                    course_data = cart_item["course"]

                    # get user paid courses library
                    user_courses_library = PaidCoursesList.objects.get(user=user)
                    course_id = course_data["id"]
                    course = Course.objects.get(id=course_id)
                    # add course to paid courses library
                    user_courses_library.courses.add(course)

                # handle product - if present in cart_item
                # TODO: check if product exists in cart_item, then handle it

            # Clear user cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart.cartitem_set.all().delete()
            cart.total_items = 0
            cart.save()

            return self.send_response(payment)
        else:
            return self.send_error("Payment failed")
