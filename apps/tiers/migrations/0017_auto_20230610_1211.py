# Generated by Django 3.2.16 on 2023-06-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0016_subscription_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='index',
        ),
        migrations.AddField(
            model_name='tier',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]