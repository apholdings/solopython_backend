# Generated by Django 3.2.16 on 2023-06-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0008_rename_features_feature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='payment_methods_allowed',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]