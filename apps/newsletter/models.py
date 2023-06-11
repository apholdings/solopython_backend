from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string


class NewsletterUser(models.Model):
    email = models.EmailField(null=False, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True, null=True)
    email = models.ManyToManyField(NewsletterUser)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Newsletter)
def send_newsletter_emails(sender, instance, created, **kwargs):
    if created:
        subject = instance.subject
        body = instance.body

        # Render the email template with the newsletter data
        email_body = render_to_string(
            "email/newsletter/welcome.html", {"newsletter": instance}
        )

        # Get the list of subscribed users
        subscribed_users = NewsletterUser.objects.all()

        # Send emails to each subscribed user
        for user in subscribed_users:
            send_mail(
                subject,
                email_body,
                "noreply@solopython.com",
                [user.email],
                fail_silently=False,
            )
