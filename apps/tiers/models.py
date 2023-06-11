from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Feature(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.title


class Tier(models.Model):
    FREQUENCY_CHOICES = [
        ("months", "Months"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    slug = models.CharField(max_length=256, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="marketplace/courses/tiers/media")
    mostPopular = models.BooleanField(blank=True, null=True)

    index = models.IntegerField(null=True, blank=True)

    features = models.ManyToManyField(Feature)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tier_creator"
    )

    tier_id = models.CharField(max_length=256)
    application_id = models.CharField(max_length=256)
    collector_id = models.CharField(max_length=256)

    external_reference = models.CharField(max_length=256, blank=True, null=True)
    init_point = models.CharField(max_length=256, blank=True, null=True)
    date_created = models.CharField(max_length=256)
    last_modified = models.CharField(max_length=256)

    reason = models.CharField(max_length=256)
    frequency = models.IntegerField()
    frequency_type = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    repetitions = models.IntegerField(blank=True, null=True)
    billing_day = models.IntegerField()
    billing_day_proportional = models.BooleanField(default=True)
    free_trial_frequency = models.IntegerField(blank=True, null=True)
    free_trial_frequency_type = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, blank=True, null=True
    )
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_amount_proportional = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    currency_id = models.CharField(max_length=3)
    payment_methods_allowed = models.JSONField(default=dict, blank=True, null=True)
    back_url = models.URLField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.reason


class Subscription(models.Model):
    subscriber = models.EmailField(max_length=256)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor")

    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name="tier")

    subscription_id = models.CharField(max_length=100)

    reason = models.CharField(max_length=100)
    external_reference = models.CharField(max_length=256)

    preapproval_plan_id = models.CharField(max_length=256)

    init_point = models.URLField()
    back_url = models.CharField(max_length=256)

    status = models.CharField(max_length=20)

    payer_id = models.CharField(max_length=256)
    card_id = models.CharField(max_length=256)
    payment_method_id = models.CharField(max_length=256)

    next_payment_date = models.CharField(max_length=256)

    date_created = models.CharField(max_length=256)
    last_modified = models.CharField(max_length=256)
