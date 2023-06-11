from rest_framework_api.views import StandardAPIView
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q, F
import requests
from rest_framework.exceptions import APIException
from apps.tiers.models import Tier

from django.conf import settings

access_token = settings.MERCADOPAGO_ACCESS_TOKEN


class CreateTierView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        url = "https://api.mercadopago.com/preapproval_plan"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "reason": request.data.get("reason"),
            "auto_recurring": {
                "frequency": int(
                    request.data.get("frequency")
                ),  # Indica el valor de la frecuencia. 7 dias, 1 meses
                "frequency_type": request.data.get("frequency_type"),  # dias, meses
                # "repetitions": 12, # se utiliza apra crear una suscripcion limitada
                "billing_day": 5,
                "billing_day_proportional": True,
                "transaction_amount": request.data.get("transaction_amount"),
                "currency_id": "PEN",
            },
            "payment_methods_allowed": {"payment_types": [{}], "payment_methods": [{}]},
            "back_url": "https://www.solopython.com/tier_created",
        }

        response = requests.post(url, headers=headers, json=payload)
        print(response.content)
        data = response.json()

        if response.status_code == 201:
            # Create the Tier instance
            tier = Tier(
                user=request.user,
                title=request.data.get("title"),
                description=request.data.get("description"),
                tier_id=data["id"],
                application_id=data["application_id"],
                collector_id=data["collector_id"],
                init_point=data["init_point"],
                date_created=data["date_created"],
                last_modified=data["last_modified"],
                reason=data["reason"],
                frequency=data["auto_recurring"]["frequency"],
                frequency_type=data["auto_recurring"]["frequency_type"],
                # repetitions=data["auto_recurring"].get("repetitions"),
                billing_day=data["auto_recurring"]["billing_day"],
                billing_day_proportional=data["auto_recurring"][
                    "billing_day_proportional"
                ],
                free_trial_frequency=data["auto_recurring"]
                .get("free_trial", {})
                .get("frequency"),
                free_trial_frequency_type=data["auto_recurring"]
                .get("free_trial", {})
                .get("frequency_type"),
                transaction_amount=data["auto_recurring"]["transaction_amount"],
                transaction_amount_proportional=data["auto_recurring"][
                    "transaction_amount_proportional"
                ],
                currency_id=data["auto_recurring"]["currency_id"],
                payment_methods_allowed=data["payment_methods_allowed"],
                back_url=data["back_url"],
                status=data["status"],
            )

            # Save the Tier instance
            tier.save()

            # Serialize the Tier instance
            serializer = TierSerializer(tier)

            # Return the serialized data
            return self.send_response(serializer.data)

        # Handle error response
        return self.send_error("Error Creating Tier")


class ListTiersView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers, many=True)
        return self.paginate_response(request, serializer.data)


class DetailTierView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        tier_id = self.request.query_params.get("tier_id")
        tier = Tier.objects.get(tier_id=tier_id)
        serializer = TierSerializer(tier)
        return self.send_response(serializer.data)


class ListUserSubscriptionsView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        email = request.user.email
        subscriptions = Subscription.objects.filter(subscriber=email)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return self.send_response(serializer.data)


class UpdateSubscritionView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = request.user
        subscription_id = request.data.get("subscription_id")
        url = f"https://api.mercadopago.com/preapproval/{subscription_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {"status": request.data.get("status")}
        response = requests.post(url, headers=headers, json=payload)
        print(response.content)
        data = response.json()
        print(data)
        subscription = Subscription.objects.get(subscription_id=subscription_id)
        # TODO: Update subscription and Take necesarry action depending on status requested
        serializer = SubscriptionSerializer(subscription)
        return self.send_response(serializer)
