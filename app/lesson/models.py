from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

User = get_user_model()


class Product(models.Model):
    """Модель продукта."""
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(
        'навзание продукта',
        max_length=40,
        unique=True
    )

    class Meta:
        """Класс Meta для Product описание метаданных."""
        ordering = ('id',)
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self) -> str:
        return self.name


class UserProduct(models.Model):
    """Класс ПользовательПродукт, Если есть в бд значит есть доступ."""
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )

    class Meta:
        """Класс Meta для UserProduct описание метаданных."""
        ordering = ('id',)
        verbose_name = 'пользователь_продукт'
        verbose_name_plural = 'пользователи_продукты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_product_userproduct'
            ),
        )

    def __str__(self) -> str:
        return f'{self.product} {self.user}'


class Lesson(models.Model):
    """Класс уроков."""
    product = models.ManyToManyField(
        Product,
        through='ProductLesson'
    )
    title = models.CharField(
        'Название урока',
        max_length=30,
        unique=True
    )
    url = models.URLField(
        'ссылка на видео',
        unique=True
    )
    total_time = models.IntegerField(
        'Длительность урока в секундах'
    )

    class Meta:
        """Класс Meta для Lesson описание метаданных."""
        ordering = ('id',)
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self) -> str:
        return self.title


class ProductLesson(models.Model):
    """Класс ПродуктУрок."""
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='урок',
        on_delete=models.CASCADE
    )

    class Meta:
        """Класс Meta для ProductLesson описание метаданных."""
        ordering = ('id',)
        verbose_name = 'продукт_урок'
        verbose_name_plural = 'продукты_уроки'

    def __str__(self) -> str:
        return f'{self.product} {self.lesson}'


class UserLesson(models.Model):
    """Класс ПользовательУрок."""
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='урок',
        on_delete=models.CASCADE
    )
    time = models.IntegerField(
        'Время просмотра.',
        default=0
    )
    date_last = models.DateTimeField(
        verbose_name='Дата просмотра',
        auto_now=True
    )

    @property
    def status(self):
        """Поле статуса."""
        percent = (self.time / self.lesson.total_time) * 100
        if percent >= 80:
            return 'Просмотрено'
        return 'Не просмотрено'

    def clean(self):
        if self.time > self.lesson.total_time:
            raise ValidationError(
                'Время не может быть больше времени урока'
            )
        qs = UserProduct.objects.filter(
            user=self.user,
            product__lesson=self.lesson,
        )
        if not qs:
            raise ValidationError({
                NON_FIELD_ERRORS: 'Нет доступа',
            })
        return super().clean()

    class Meta:
        """Класс Meta для UserLesson описание метаданных."""
        ordering = ('id',)
        verbose_name = 'пользователь_урок'
        verbose_name_plural = 'пользователи_уроки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'lesson'),
                name='unique_user_lesson_userlesson'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} {self.lesson}'
