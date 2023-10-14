from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    """Модель продукта."""
    user = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.PROTECT,
    )
    title = models.CharField(
        'Навзание продукта',
        max_length=40,
    )


class ProductAccess(models.Model):
    """Класс ПользовательПродукт, Если есть в бд значит есть доступ."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Продукт',
        related_name='accesses',
    )
    is_valid = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.product} {self.user}'
