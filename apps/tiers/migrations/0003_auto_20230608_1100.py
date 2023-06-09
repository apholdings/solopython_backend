# Generated by Django 3.2.16 on 2023-06-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0002_tier_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tier',
            name='status',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tier',
            name='free_trial_frequency_type',
            field=models.CharField(choices=[('months', 'Months')], max_length=10),
        ),
        migrations.AlterField(
            model_name='tier',
            name='frequency_type',
            field=models.CharField(choices=[('months', 'Months')], max_length=10),
        ),
    ]
