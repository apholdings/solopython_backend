from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from rest_framework import status
from .models import *
from apps.coupons.models import Coupon
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.parsers import JSONParser
from decimal import Decimal
import requests
from django.core.cache import cache
from django.conf import settings

taxes = settings.TAXES


# Create your views here.
class GetItemsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        cart = Cart.objects.get(user=user)

        total_items = cart.total_items

        cart_items = CartItem.objects.filter(cart=cart)
        serialized_cart_items = CartItemSerializer(cart_items, many=True).data

        return self.send_response(
            {
                "cart": serialized_cart_items,
                "total_items": total_items,
            },
            status=status.HTTP_200_OK,
        )


class GetTotalView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        if not data:
            return self.send_response(
                {
                    "total_cost": 0,
                    "total_cost_ethereum": 0,
                    "maticCost": 0,
                    "total_compare_cost": 0,
                    "finalPrice": 0,
                    "tax_estimate": 0,
                    "shipping_estimate": 0,
                },
                status=status.HTTP_200_OK,
            )

        courses = []
        products = []
        tiers = []
        total_cost = Decimal(0)
        total_compare_cost = Decimal(0)
        tax_estimate = Decimal(0)
        shipping_estimate = Decimal(0)
        finalProductPrice = Decimal(0)
        finalCoursePrice = Decimal(0)
        finalTierPrice = Decimal(0)
        finalPrice = Decimal(0)

        for item in data.get("items"):
            if item.get("course"):
                courses.append(item)
            elif item.get("product"):
                products.append(item)
            elif item.get("tier"):
                tiers.append(item)

        for object in courses:
            course = object["course"] if object["course"] else None
            coupon = object["coupon"] if object["coupon"] else None

            if coupon:
                coupon_fixed_price_coupon = coupon.get("fixed_price_coupon")
                coupon_percentage_coupon = coupon.get("percentage_coupon")

                if coupon_fixed_price_coupon:
                    coupon_fixed_discount_price = coupon_fixed_price_coupon.get(
                        "discount_price"
                    )

                else:
                    coupon_fixed_discount_price = None

                if coupon_percentage_coupon:
                    coupon_discount_percentage = coupon_percentage_coupon.get(
                        "discount_percentage"
                    )

                else:
                    coupon_discount_percentage = None
            else:
                coupon_fixed_price_coupon = None
                coupon_fixed_discount_price = None
                coupon_percentage_coupon = None
                coupon_discount_percentage = None

            course_price = course.get("price")
            course_compare_price = course.get("compare_price", course_price)
            course_discount = course.get("discount", False)

            # Calculate Total Cost Without Discounts and Coupons and Taxes (total_cost)
            if course_discount == False:
                total_cost += Decimal(course_price)
            else:
                total_cost += Decimal(course_compare_price)

            # Calculate Total Cost With Discount and Coupons if present (total_compare_cost)
            if course_discount == True:
                if coupon_fixed_discount_price is not None:
                    total_compare_cost += max(
                        Decimal(course_compare_price)
                        - Decimal(coupon_fixed_discount_price),
                        0,
                    )
                elif coupon_discount_percentage is not None:
                    total_compare_cost += Decimal(course_compare_price) * (
                        1 - (Decimal(coupon_discount_percentage) / 100)
                    )
                else:
                    total_compare_cost += Decimal(course_compare_price)
            else:
                if coupon_fixed_discount_price is not None:
                    total_compare_cost += max(
                        Decimal(course_price) - Decimal(coupon_fixed_discount_price), 0
                    )
                elif coupon_discount_percentage is not None:
                    total_compare_cost += Decimal(course_price) * (
                        1 - (Decimal(coupon_discount_percentage) / 100)
                    )
                else:
                    total_compare_cost += Decimal(course_price)

            # Calculate Taxes for Total Cost (tax_estimate)
            tax_estimate = Decimal(total_compare_cost) * Decimal(taxes)
            # print('Tax Estimate: ',tax_estimate )
            finalCoursePrice = Decimal(total_compare_cost) + Decimal(tax_estimate)

        for object in tiers:
            tier = object["tier"] if object["tier"] else None
            coupon = object["coupon"] if object["coupon"] else None

            if coupon:
                coupon_fixed_price_coupon = coupon.get("fixed_price_coupon")
                coupon_percentage_coupon = coupon.get("percentage_coupon")

                if coupon_fixed_price_coupon:
                    coupon_fixed_discount_price = coupon_fixed_price_coupon.get(
                        "discount_price"
                    )

                else:
                    coupon_fixed_discount_price = None

                if coupon_percentage_coupon:
                    coupon_discount_percentage = coupon_percentage_coupon.get(
                        "discount_percentage"
                    )

                else:
                    coupon_discount_percentage = None
            else:
                coupon_fixed_price_coupon = None
                coupon_fixed_discount_price = None
                coupon_percentage_coupon = None
                coupon_discount_percentage = None

            tier_price = tier.get("transaction_amount")
            tier_compare_price = tier.get("compare_price", tier_price)
            tier_discount = tier.get("discount", False)

            # Calculate Total Cost Without Discounts and Coupons and Taxes (total_cost)
            if tier_discount == False:
                total_cost += Decimal(tier_price)
            else:
                total_cost += Decimal(tier_compare_price)

            # Calculate Total Cost With Discount and Coupons if present (total_compare_cost)
            if tier_discount == True:
                if coupon_fixed_discount_price is not None:
                    total_compare_cost += max(
                        Decimal(tier_compare_price)
                        - Decimal(coupon_fixed_discount_price),
                        0,
                    )
                elif coupon_discount_percentage is not None:
                    total_compare_cost += Decimal(tier_compare_price) * (
                        1 - (Decimal(coupon_discount_percentage) / 100)
                    )
                else:
                    total_compare_cost += Decimal(tier_compare_price)
            else:
                if coupon_fixed_discount_price is not None:
                    total_compare_cost += max(
                        Decimal(tier_price) - Decimal(coupon_fixed_discount_price), 0
                    )
                elif coupon_discount_percentage is not None:
                    total_compare_cost += Decimal(tier_price) * (
                        1 - (Decimal(coupon_discount_percentage) / 100)
                    )
                else:
                    total_compare_cost += Decimal(tier_price)

            # Calculate Taxes for Total Cost (tax_estimate)
            tax_estimate = Decimal(total_compare_cost) * Decimal(taxes)
            # print('Tax Estimate: ',tax_estimate )
            finalTierPrice = Decimal(total_compare_cost) + Decimal(tax_estimate)

        finalPrice = (
            Decimal(finalProductPrice)
            + Decimal(finalCoursePrice)
            + Decimal(finalTierPrice)
        )

        eth_price = cache.get("eth_price")
        matic_price = cache.get("matic_price")
        if not eth_price:
            eth_price_response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=matic-network%2Cethereum&vs_currencies=usd"
            ).json()
            eth_price = eth_price_response.get("ethereum").get("usd")
            matic_price = eth_price_response.get("matic-network").get("usd")
            cache.set("eth_price", eth_price, 1 * 60)  # cache for 1 minutes
            cache.set("matic_price", matic_price, 1 * 60)  # cache for 1 minutes
        ethCost = finalPrice / Decimal(eth_price)
        maticCost = finalPrice / Decimal(matic_price)

        return self.send_response(
            {
                "total_cost": total_cost,
                "total_cost_ethereum": ethCost,
                "maticCost": maticCost,
                "total_compare_cost": total_compare_cost,
                "finalPrice": finalPrice,
                "tax_estimate": tax_estimate,
                "shipping_estimate": shipping_estimate,
            },
            status=status.HTTP_200_OK,
        )


class AddItemView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        data = request.data

        print(data)

        item_id = data["itemID"]
        item_type = data["type"]
        coupon_id = (
            data.get("coupon", {}).get("id") if data.get("coupon").get("id") else None
        )
        cart, created = Cart.objects.get_or_create(user=user)

        total_items = cart.total_items or 0

        if item_type == "Course":
            course = Course.objects.get(id=item_id)
            # Check if item already in cart
            if CartItem.objects.filter(cart=cart, course=course).exists():
                return self.send_error(
                    "Item is already in cart", status=status.HTTP_409_CONFLICT
                )

            cart_item_object = CartItem.objects.create(course=course, cart=cart)

            if data.get("coupon").get("id") is not None:
                # Get the coupon object
                coupon = Coupon.objects.get(id=coupon_id)

                # Validate that the coupon applies to the course
                if coupon.content_type != "courses" or coupon.course != course:
                    return self.send_error(
                        "Coupon does not apply to this course",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cart_item_object.coupon = coupon
                cart_item_object.save()

            # Check for referrer and save it if present
            if "referrer" in data:
                referrer = data["referrer"]
                cart_item_object.referrer = referrer
                cart_item_object.save()

            if CartItem.objects.filter(cart=cart, course=item_id).exists():
                # Update the total number of items in the cart
                total_items = int(cart.total_items) + 1
                Cart.objects.filter(user=user).update(total_items=total_items)

        if item_type == "Tier":
            tier = Tier.objects.get(id=item_id)
            # Check if item already in cart
            if CartItem.objects.filter(cart=cart, tier=tier).exists():
                return self.send_error(
                    "Item is already in cart", status=status.HTTP_409_CONFLICT
                )

            cart_item_object = CartItem.objects.create(tier=tier, cart=cart)

            if data.get("coupon").get("id") is not None:
                # Get the coupon object
                coupon = Coupon.objects.get(id=coupon_id)

                # Validate that the coupon applies to the course
                if coupon.content_type != "tiers" or coupon.tier != tier:
                    return self.send_error(
                        "Coupon does not apply to this tier",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cart_item_object.coupon = coupon
                cart_item_object.save()

            # Check for referrer and save it if present
            if "referrer" in data:
                referrer = data["referrer"]
                cart_item_object.referrer = referrer
                cart_item_object.save()

            if CartItem.objects.filter(cart=cart, tier=tier).exists():
                # Update the total number of items in the cart
                total_items = int(total_items) + 1
                Cart.objects.filter(user=user).update(total_items=total_items)

        cart_items = CartItem.objects.filter(cart=cart)
        serialized_cart_items = CartItemSerializer(cart_items, many=True).data

        return self.send_response(
            {"cart": serialized_cart_items, "total_items": total_items},
            status=status.HTTP_200_OK,
        )


class RemoveItemView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        data = request.data

        item_id = data["itemID"]
        item_type = data["type"]
        cart, _ = Cart.objects.get_or_create(user=user)

        if item_type == "Course":
            course = Course.objects.get(id=item_id)
            cart_item = CartItem.objects.filter(cart=cart, course=course)

            if not cart_item.exists():
                return self.send_error(
                    "Item is not in cart", status=status.HTTP_404_NOT_FOUND
                )

            cart_item.delete()

            # Update the total number of items in the cart
            total_items = max(0, int(cart.total_items) - 1)
            Cart.objects.filter(user=user).update(total_items=total_items)

        if item_type == "Tier":
            tier = Tier.objects.get(id=item_id)
            cart_item = CartItem.objects.filter(cart=cart, tier=tier)

            if not cart_item.exists():
                return self.send_error(
                    "Item is not in cart", status=status.HTTP_404_NOT_FOUND
                )

            cart_item.delete()

            # Update the total number of items in the cart
            total_items = max(0, int(cart.total_items) - 1)
            Cart.objects.filter(user=user).update(total_items=total_items)

        cart_items = CartItem.objects.filter(cart=cart)
        serialized_cart_items = CartItemSerializer(cart_items, many=True).data

        return self.send_response(
            {"cart": serialized_cart_items, "total_items": total_items},
            status=status.HTTP_200_OK,
        )


class ClearCartView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
        cart.total_items = 0
        cart.save()
        serializer = CartSerializer(cart)
        return self.send_response(serializer.data, status=status.HTTP_200_OK)


class SynchCartItemsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        items = []
        courses = []
        products = []
        tiers = []

        data = request.data

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = data["items"]

        # Clear all existing items in the cart
        cart.cartitem_set.all().delete()

        for item in cart_items:
            if item["type"] == "Course":
                courses.append(item)
            elif item["type"] == "Product":
                products.append(item)
            elif item["type"] == "Tier":
                tiers.append(item)

        # Add courses to the cart
        for course_data in courses:
            course = Course.objects.get(id=course_data["course"]["id"])

            coupon_id = course_data.get("coupon").get("id")
            if coupon_id is not None:
                coupon = Coupon.objects.get(id=coupon_id)
            else:
                coupon = None

            # create and save the cart item
            item = CartItem(
                cart=cart,
                course=course,
                coupon=coupon,
                referrer=course_data.get("referrer"),
            )
            item.save()

            items.append(item)

        # Add courses to the cart
        for tier_data in tiers:
            tier = Tier.objects.get(id=tier_data["tier"]["id"])

            coupon_id = tier_data.get("coupon").get("id")
            if coupon_id is not None:
                coupon = Coupon.objects.get(id=coupon_id)
            else:
                coupon = None

            # create and save the cart item
            item = CartItem(
                cart=cart,
                tier=tier,
                coupon=coupon,
                referrer=tier_data.get("referrer"),
            )
            item.save()

            items.append(item)

        # calculate total_items based on newly added items
        cart.total_items = CartItem.objects.filter(cart=cart).count()
        cart.save()

        cart_items = CartItem.objects.filter(cart=cart)
        serialized_cart_items = CartItemSerializer(cart_items, many=True).data

        return self.send_response(
            {"cart": serialized_cart_items, "total_items": cart.total_items},
            status=status.HTTP_200_OK,
        )
