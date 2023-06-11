# Generated by Django 3.2.16 on 2023-06-08 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0011_tier_thumbnail'),
        ('coupons', '0003_coupon_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tiers.tier'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='content_type',
            field=models.CharField(choices=[('courses', 'Courses'), ('products', 'Products'), ('tiers', 'Tiers'), ('games', 'Games'), ('music', 'Music'), ('videos', 'Videos'), ('movies', 'Movies'), ('assets', 'Assets'), ('art', 'Art'), ('software', 'Software'), ('licenseKeys', 'License Keys'), ('documents', 'Documents'), ('datasets', 'Datasets'), ('templates', 'Templates')], default='courses', max_length=20),
        ),
    ]
