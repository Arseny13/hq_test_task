import datetime

from django.db import models
from django.contrib.auth import get_user_model

from catalog.models import Product

User = get_user_model()


class Lesson(models.Model):
    """Класс уроков."""
    products = models.ManyToManyField(
        Product,
    )
    title = models.CharField(
        'Название урока',
        max_length=30,
        unique=True
    )
    video_url = models.URLField(
        'ссылка на видео',
        unique=True
    )
    video_duration = models.IntegerField(
        'Длительность урока в секундах',
        default=0
    )

    class Meta:
        """Класс Meta для Lesson описание метаданных."""
        ordering = ('id',)
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self) -> str:
        return self.title


class LessonStatusEnum(models.TextChoices):
    VIEWED = 'VIEWED'
    NOT_VIEWED = 'NOT_VIEWED'


class LessonViewInfo(models.Model):
    """Класс ПользовательУрок."""
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Урок',
        related_name='views',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='lesson'
    )
    status = models.CharField(
        choices=LessonStatusEnum.choices,
        default=LessonStatusEnum.NOT_VIEWED,
        max_length=30,
    )
    view_time = models.IntegerField(
        'Время просмотра',
        default=0
    )
    last_view_datetime = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        unique_together = ('lesson', 'user')
