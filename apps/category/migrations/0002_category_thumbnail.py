# Generated by Django 3.2.16 on 2023-06-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='categories/thumbnail'),
        ),
    ]
