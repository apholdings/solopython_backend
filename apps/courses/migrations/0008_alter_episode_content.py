# Generated by Django 3.2.16 on 2023-06-08 05:24

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_question_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
