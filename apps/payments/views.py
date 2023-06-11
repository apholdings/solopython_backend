from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
import mercadopago
from django.conf import settings
from apps.coupons.models import Coupon
from apps.courses.models import PaidCoursesList, Course
from apps.cart.models import Cart, CartItem
from apps.tiers.models import *
from apps.cart.serializers import *
import requests
from typing import List
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()

access_token = settings.MERCADOPAGO_ACCESS_TOKEN
sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


class CreditCardPaymentView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user

        data = request.data
        cart = data["cart"]
        token = data["token"]
        transaction_amount = data["transaction_amount"]
        payer = data["payer"]
        email = payer.get("email")

        issuer_id = data["issuer_id"]
        payment_method_id = data["payment_method_id"]
        installments = data["installments"]
        identification_type = payer.get("identification").get("type")
        identification_number = payer.get("identification").get("number")

        payments: List[dict] = []

        cart_object = Cart.objects.get(user=request.user)

        # Handle Subscriptions Tier Payments
        for cart_item in cart:
            if cart_item.get("tier") is not None:
                # Obtener Plan que se compra
                tier = Tier.objects.get(tier_id=cart_item["tier"]["tier_id"])

                url = "https://api.mercadopago.com/preapproval"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "preapproval_plan_id": tier.tier_id,
                    "reason": tier.reason,
                    "payer_email": email,
                    "card_token_id": token,
                    "auto_recurring": {
                        "frequency": tier.frequency,
                        "frequency_type": tier.frequency_type,
                        # "start_date": "2020-06-02T13:07:14.260Z",
                        # "end_date": "2022-07-20T15:59:52.581Z",
                        "transaction_amount": int(tier.transaction_amount),
                        "currency_id": tier.currency_id,
                    },
                    "back_url": "https://www.solopython.com/payment_successful",
                    "status": "authorized",
                }
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    # print("Response ", response)
                    # print("Response Content ", response.content)
                    data = response.json()
                    if data.get("status") == "authorized":
                        # Deduce precio del item comprado del precio total a pagar del carrito
                        transaction_amount -= float(tier.transaction_amount)

                        Subscription.objects.create(
                            subscriber=email,
                            vendor=tier.user,
                            tier=tier,
                            subscription_id=data["id"],
                            reason=data["reason"],
                            external_reference=data["preapproval_plan_id"],
                            preapproval_plan_id=data["preapproval_plan_id"],
                            init_point=data["init_point"],
                            back_url=data["back_url"],
                            status=data["status"],
                            payer_id=data["payer_id"],
                            card_id=data["card_id"],
                            payment_method_id=data["payment_method_id"],
                            next_payment_date=data["next_payment_date"],
                            date_created=data["date_created"],
                            last_modified=data["last_modified"],
                        )

                        # Remove product from cart
                        cart_item_object = CartItem.objects.get(id=cart_item["id"])
                        cart_item_object.delete()
                        cart_object.total_items -= 1
                        cart_object.save()
                except Exception as e:
                    print("Response ", response)
                    print("Response Content ", response.content)
                    # Handle the exception gracefully (e.g., log the error, return a default response)
                    # You can also raise the exception again if you want to propagate it further
                    # or customize the handling based on the specific error encountered
                    print(f"Subscription Payment creation failed: {str(e)}")

        # Handle Single Cart Payments
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
        print(payment)
        payments.append(payment)

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

                # Remove product from cart
                cart_object = Cart.objects.get(user=request.user)
                cart_item_object = CartItem.objects.get(id=cart_item["id"])
                cart_item_object.delete()
                cart_object.total_items -= 1
                cart_object.save()

            cart = Cart.objects.get(user=request.user)
            cart_serializer = CartSerializer(cart)
            return self.send_response(cart_serializer.data)
        else:
            print("Payment Failed")
            return self.send_error("Payment failed")
