# Generated by Django 3.2.16 on 2023-06-09 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0012_auto_20230609_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_created',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='last_modified',
            field=models.CharField(max_length=256),
        ),
    ]
