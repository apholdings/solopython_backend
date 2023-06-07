from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from decimal import Decimal
from .helpers import get_timer
from mutagen.mp4 import MP4, MP4StreamInfoError
from django.utils import timezone
from apps.category.models import Category

from djoser.signals import user_registered

from django.conf import settings

User = settings.AUTH_USER_MODEL


def course_directory_path(instance, filename):
    return "marketplace/courses/{0}/{1}".format(instance.title, filename)


def sector_directory_path(instance, filename):
    return "marketplace/courses/sector/{0}/{1}".format(instance.title, filename)


def chapter_directory_path(instance, filename):
    return "marketplace/courses/{0}/{1}/{2}".format(
        instance.course, instance.title, filename
    )


def lesson_directory_path(instance, filename):
    return "marketplace/courses/{0}/{1}/Lesson #{2}: {3}/{4}".format(
        instance.course,
        instance.chapter,
        instance.number,
        instance.title,
        filename,
    )


class Media(models.Model):
    MEDIA_TYPES = (
        ("image", "Image"),
        ("document", "Document"),
        ("video", "Video"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=60, blank=True, null=True)
    file = models.FileField(
        upload_to="marketplace/courses/media"
    )  # changed to FileField
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)


class Sellers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.author.username


class Course(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    languages = (
        ("español", "Español"),
        ("ingles", "Ingles"),
    )

    payment_options = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    token_id = models.TextField(unique=True, blank=True, null=True)
    nft_address = models.CharField(default=0, max_length=256, blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="course_author",
    )
    sellers = models.ManyToManyField(Sellers, blank=True, related_name="courseSellers")

    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    short_description = models.TextField(max_length=169, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    images = models.ManyToManyField(
        Media,
        blank=True,
        related_name="course_images",
        limit_choices_to={"media_type": "image"},
    )
    videos = models.ManyToManyField(
        Media,
        blank=True,
        related_name="course_videos",
        limit_choices_to={"media_type": "video"},
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="courses",
    )
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="sub_category_courses",
    )
    topic = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="topic_courses",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.ManyToManyField("Rate", blank=True, related_name="courseRating")
    student_rating = models.IntegerField(default=0, blank=True, null=True)

    stock = models.IntegerField(default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    compare_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    discount_until = models.DateTimeField(default=timezone.now, blank=True, null=True)
    discount = models.BooleanField(default=False)
    payment = models.CharField(
        max_length=100, choices=payment_options, default="unpaid"
    )

    language = models.CharField(max_length=50, choices=languages, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    taught = models.CharField(max_length=120, blank=True, null=True)

    welcome_message = models.CharField(max_length=1200, blank=True, null=True)
    congrats_message = models.CharField(max_length=1200, blank=True, null=True)

    sold = models.IntegerField(default=0, blank=True)
    course_length = models.CharField(default=0, max_length=20, blank=True, null=True)
    students = models.IntegerField(default=0, blank=True)
    views = models.IntegerField(default=0, blank=True)

    best_seller = models.BooleanField(default=False)

    # Course Creation Booleans
    goals = models.BooleanField(default=False)
    course_structure = models.BooleanField(default=False)
    setup = models.BooleanField(default=False)
    film = models.BooleanField(default=False)
    curriculum = models.BooleanField(default=False)
    captions = models.BooleanField(default=False)
    accessibility = models.BooleanField(default=False)
    landing_page = models.BooleanField(default=False)
    pricing = models.BooleanField(default=False)
    promotions = models.BooleanField(default=False)
    allow_messages = models.BooleanField(default=False)

    analytics = models.OneToOneField(
        "CourseAnalytics",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="course_analytics",
    )

    can_delete = models.BooleanField(default=True)
    banned = models.BooleanField(default=False)

    sections = models.ManyToManyField(
        "Section", blank=True, related_name="section_from_course"
    )
    what_learnt = models.ManyToManyField(
        "WhatLearnt", blank=True, related_name="whatlearnt_from_course"
    )
    requisites = models.ManyToManyField(
        "Requisite", blank=True, related_name="requisite_from_course"
    )
    who_is_for = models.ManyToManyField(
        "WhoIsFor", blank=True, related_name="whoisfor_from_course"
    )
    resources = models.ManyToManyField(
        "Resource", blank=True, related_name="resources_from_course"
    )

    status = models.CharField(max_length=10, choices=options, default="draft")

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.title

    def get_first_image(self):
        if self.images.exists():
            return self.images.first().file.url
        return None

    def get_first_video(self):
        if self.videos.exists():
            return self.videos.first().file.url
        return None

    def progress(self):
        progress = 0
        if self.goals:
            progress += 1
        if self.course_structure:
            progress += 1
        if self.setup:
            progress += 1
        if self.film:
            progress += 1
        if self.curriculum:
            progress += 1
        if self.captions:
            progress += 1
        if self.accessibility:
            progress += 1
        if self.landing_page:
            progress += 1
        if self.pricing:
            progress += 1
        if self.promotions:
            progress += 1
        if self.allow_messages:
            progress += 1
        # other fields
        return progress

    def get_rating(self):
        ratings = self.rating.all()
        rate = 0
        for rating in ratings:
            rate += rating.rate_number
        try:
            rate /= len(ratings)
        except ZeroDivisionError:
            rate = 0
        return rate

    def get_no_rating(self):
        return len(self.rating.all())

    def get_whatlearnt(self):
        return WhatLearnt.objects.filter(course=self)[:4]

    def get_requisites(self):
        return len(self.requisite.all())

    def get_videos(self):
        return len(self.videos.all())

    def get_images(self):
        return len(self.images.all())

    def get_brief_description(self):
        return self.description[:100]

    def get_total_lectures(self):
        lectures = 0
        for section in self.sections.all():
            lectures += len(section.episodes.all())
        return lectures

    def total_course_length(self):
        length = Decimal(0.00)
        for section in self.sections.all():
            for episode in section.episodes.all():
                length += episode.length
        return get_timer(length)

    def get_category_name(self):
        if self.category:
            name = self.category.name
            return name
        else:
            return

    def get_view_count(self):
        game_views = ViewCount.objects.filter(post=self).count()
        return game_views


class CourseAnalytics(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="course_analytics_reverse",
    )
    views = models.IntegerField(default=0, blank=True)
    clicks = models.IntegerField(default=0, blank=True, null=True)
    impressions = models.IntegerField(default=0, blank=True, null=True)
    clickThroughRate = models.FloatField(default=0, blank=True, null=True)
    purchases = models.IntegerField(default=0, blank=True, null=True)
    conversion_rate = models.FloatField(default=0, blank=True, null=True)
    avg_time_on_page = models.FloatField(default=0, blank=True, null=True)
    sold = models.IntegerField(default=0, blank=True, null=True)
    income_earned = models.PositiveIntegerField(default=0, blank=True)


class ViewCount(models.Model):
    course = models.ForeignKey(
        Course, related_name="course_view_count", on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"


class Rate(models.Model):
    rate_number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_rate"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="rate_belongs_to_course",
        blank=True,
        null=True,
    )


class Requisite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_requisite"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="requisite_belongs_to_course",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class WhatLearnt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_whatlearnt"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="whatlearnt_belongs_to_course",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class WhoIsFor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_whoisfor"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="whoisfor_belongs_to_course",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    learning_objective = models.CharField(max_length=1200, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    episodes = models.ManyToManyField("Episode", blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_section"
    )
    published = models.BooleanField(default=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="section_belongs_to_course",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("number",)

    def __str__(self):
        return self.title

    def total_length(self):
        total = Decimal(0.00)
        for episode in self.episodes.all():
            total += episode.length
        return get_timer(total, type="min")


class Episode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="episodes", blank=True, null=True)
    filename = models.CharField(max_length=1200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=1200, blank=True, null=True)
    length = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    free = models.BooleanField(default=False, blank=True, null=True)
    resources = models.ManyToManyField("Resource", blank=True)
    questions = models.ManyToManyField(
        "Question", blank=True, related_name="episode_questions"
    )
    comments = models.ManyToManyField(
        "Comment", blank=True, related_name="episode_comments"
    )
    number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_episode"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="episode_belongs_to_course",
        blank=True,
        null=True,
    )
    section_uuid = models.UUIDField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    published = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ("number",)

    def __str__(self):
        return self.title

    def get_video_length(self):
        if self.file:
            try:
                video = MP4(self.file)
                return video.info.length

            except MP4StreamInfoError:
                return 0.0
        else:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def get_absolute_url(self):
        if self.file:
            return self.file.url

    def save(self, *args, **kwargs):
        self.length = self.get_video_length()
        return super().save(*args, **kwargs)


class EpisodeCompletion(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_episode_complete"
    )
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=course_directory_path, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_resource"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_comment"
    )
    body = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField("Like", blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(
        "Like", blank=True, related_name="comment_dislikes"
    )

    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        related_name="episode_comments",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-created_at",)

    # def __str__(self):
    #     return self.episode.title

    def liked_by_user(self):
        is_like = False
        for like in self.likes.all():
            if like.user == self.user:
                is_like = True
        return is_like

    def disliked_by_user(self):
        is_dislike = False
        for dislike in self.dislikes.all():
            if dislike.user == self.user:
                is_dislike = True
        return is_dislike

    def likes_count(self):
        likes_count = self.likes.count()
        return likes_count

    def dislikes_count(self):
        dislikes_count = self.dislikes.count()
        return dislikes_count


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_question"
    )
    title = models.CharField(max_length=120)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    episode = models.ForeignKey(
        "Episode",
        on_delete=models.CASCADE,
        related_name="episode_belongs_to_question",
        blank=True,
        null=True,
    )
    correct_answer = models.ForeignKey(
        "Answer",
        on_delete=models.CASCADE,
        related_name="correct_answer",
        null=True,
        blank=True,
    )
    update_date = models.DateTimeField(auto_now_add=True)
    has_accepted_answer = models.BooleanField(default=False)
    likes = models.ManyToManyField("Like", blank=True, related_name="question_likes")
    dislikes = models.ManyToManyField(
        "Like", blank=True, related_name="question_dislikes"
    )

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.title

    def liked_by_user(self):
        is_like = False
        for like in self.likes.all():
            if like.user == self.user:
                is_like = True
        return is_like

    def disliked_by_user(self):
        is_dislike = False
        for dislike in self.dislikes.all():
            if dislike.user == self.user:
                is_dislike = True
        return is_dislike

    def likes_count(self):
        likes_count = self.likes.count()
        return likes_count

    def dislikes_count(self):
        dislikes_count = self.dislikes.count()
        return dislikes_count

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_answers(self):
        return Answer.objects.filter(question=self)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_course_question_answer"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    is_accepted_answer = models.BooleanField(default=False)
    likes = models.ManyToManyField("Like", blank=True, related_name="answer_likes")
    dislikes = models.ManyToManyField(
        "Like", blank=True, related_name="answer_dislikes"
    )

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.question.title

    def liked_by_user(self):
        is_like = False
        for like in self.likes.all():
            if like == self.user:
                is_like = True
        return is_like

    def disliked_by_user(self):
        is_dislike = False
        for dislike in self.dislikes.all():
            if dislike.user == self.user:
                is_dislike = True
        return is_dislike

    def likes_count(self):
        likes_count = self.likes.count()
        return likes_count

    def dislikes_count(self):
        dislikes_count = self.dislikes.count()
        return dislikes_count


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_liked_course"
    )


class Dislike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_disliked_course"
    )


class ViewedCoursesLibrary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_viewed_courses_library"
    )
    courses = models.ManyToManyField(Course, blank=True)

    class Meta:
        verbose_name_plural = "Viewed Courses"

    def __str__(self):
        return self.user


class Viewed(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_viewed_course"
    )
    date_created = models.DateTimeField(auto_now_add=True)


class ViewedItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    library = models.ForeignKey(Viewed, on_delete=models.CASCADE)
    course = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class PaidCoursesList(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_paid_courses_list"
    )
    courses = models.ManyToManyField(Course)
    created_at = models.DateTimeField(auto_now_add=True)


class WishList(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_courses_wishlist"
    )
    total_items = models.IntegerField(default=0)
    courses = models.ManyToManyField("Course")
    date_created = models.DateTimeField(auto_now_add=True)


def post_user_registered(request, user, *args, **kwargs):
    # 1. Definir usuario que ser registra
    user = user
    PaidCoursesList.objects.create(user=user)
    WishList.objects.create(user=user)
    ViewedCoursesLibrary.objects.create(user=user)


user_registered.connect(post_user_registered)
