# Generated by Django 3.2.16 on 2023-06-08 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0011_tier_thumbnail'),
        ('cart', '0004_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='tier',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='tiers.tier'),
            preserve_default=False,
        ),
    ]
