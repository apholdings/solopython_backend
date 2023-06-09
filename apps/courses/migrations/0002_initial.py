# Generated by Django 3.2.16 on 2023-06-05 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_courses_wishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='whoisfor',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whoisfor_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='whoisfor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_whoisfor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='whatlearnt',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whatlearnt_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='whatlearnt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_whatlearnt', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vieweditem',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vieweditem',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.viewed'),
        ),
        migrations.AddField(
            model_name='viewedcourseslibrary',
            name='courses',
            field=models.ManyToManyField(blank=True, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='viewedcourseslibrary',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_viewed_courses_library', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='viewed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_viewed_course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='viewcount',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_view_count', to='courses.course'),
        ),
        migrations.AddField(
            model_name='sellers',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='section',
            name='episodes',
            field=models.ManyToManyField(blank=True, to='courses.Episode'),
        ),
        migrations.AddField(
            model_name='section',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_section', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_resource', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requisite',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requisite_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='requisite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_requisite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rate',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rate_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_rate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correct_answer', to='courses.answer'),
        ),
        migrations.AddField(
            model_name='question',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='question_dislikes', to='courses.Like'),
        ),
        migrations.AddField(
            model_name='question',
            name='episode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episode_belongs_to_question', to='courses.episode'),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='question_likes', to='courses.Like'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_question', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paidcourseslist',
            name='courses',
            field=models.ManyToManyField(to='courses.Course'),
        ),
        migrations.AddField(
            model_name='paidcourseslist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_paid_courses_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='media',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_liked_course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='episodecompletion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='episodecompletion',
            name='episode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.episode'),
        ),
        migrations.AddField(
            model_name='episodecompletion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_episode_complete', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='episode',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episode_belongs_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='episode',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='episode_questions', to='courses.Question'),
        ),
        migrations.AddField(
            model_name='episode',
            name='resources',
            field=models.ManyToManyField(blank=True, to='courses.Resource'),
        ),
        migrations.AddField(
            model_name='episode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_episode', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_disliked_course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='category.category'),
        ),
        migrations.AddField(
            model_name='course',
            name='images',
            field=models.ManyToManyField(blank=True, limit_choices_to={'media_type': 'image'}, related_name='course_images', to='courses.Media'),
        ),
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.ManyToManyField(blank=True, related_name='courseRating', to='courses.Rate'),
        ),
        migrations.AddField(
            model_name='course',
            name='requisites',
            field=models.ManyToManyField(blank=True, related_name='requisite_from_course', to='courses.Requisite'),
        ),
        migrations.AddField(
            model_name='course',
            name='resources',
            field=models.ManyToManyField(blank=True, related_name='resources_from_course', to='courses.Resource'),
        ),
        migrations.AddField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='section_from_course', to='courses.Section'),
        ),
        migrations.AddField(
            model_name='course',
            name='sellers',
            field=models.ManyToManyField(blank=True, related_name='courseSellers', to='courses.Sellers'),
        ),
        migrations.AddField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_category_courses', to='category.category'),
        ),
        migrations.AddField(
            model_name='course',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='topic_courses', to='category.category'),
        ),
        migrations.AddField(
            model_name='course',
            name='videos',
            field=models.ManyToManyField(blank=True, limit_choices_to={'media_type': 'video'}, related_name='course_videos', to='courses.Media'),
        ),
        migrations.AddField(
            model_name='course',
            name='what_learnt',
            field=models.ManyToManyField(blank=True, related_name='whatlearnt_from_course', to='courses.WhatLearnt'),
        ),
        migrations.AddField(
            model_name='course',
            name='who_is_for',
            field=models.ManyToManyField(blank=True, related_name='whoisfor_from_course', to='courses.WhoIsFor'),
        ),
        migrations.AddField(
            model_name='answer',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='answer_dislikes', to='courses.Like'),
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='answer_likes', to='courses.Like'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_question_answer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='analytics',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_analytics', to='courses.courseanalytics'),
        ),
    ]
