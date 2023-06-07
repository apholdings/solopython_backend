# Generated by Django 3.2.16 on 2023-06-05 17:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('content_type', models.CharField(choices=[('courses', 'Courses'), ('products', 'Products'), ('games', 'Games'), ('music', 'Music'), ('videos', 'Videos'), ('movies', 'Movies'), ('assets', 'Assets'), ('art', 'Art'), ('software', 'Software'), ('licenseKeys', 'License Keys'), ('documents', 'Documents'), ('datasets', 'Datasets'), ('templates', 'Templates')], default='courses', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='FixedPriceCoupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('uses', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PercentageCoupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('discount_percentage', models.IntegerField()),
                ('uses', models.IntegerField()),
            ],
        ),
    ]