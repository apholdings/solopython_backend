# Generated by Django 3.2.16 on 2023-06-05 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0002_cartitem_coupon'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]