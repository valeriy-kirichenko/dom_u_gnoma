from django.core.validators import MinValueValidator
from django.db import models
from typing import Tuple

from .utils import image_directory_path
from users.models import User


class Item(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    description = models.TextField('Описание',)
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    image = models.ImageField('Картинка', upload_to=image_directory_path)
    weight = models.IntegerField(
        'Вес(гр)',
        blank=True,
        null=True,
        validators=(
            MinValueValidator(0, 'Вес не может быть отрицательным'),
        )
    )

    class Meta:
        ordering: Tuple[str] = ('id',)
        verbose_name: str = 'Изделие'
        verbose_name_plural: str = 'Изделия'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return self.name


class Cart(models.Model):
    """Модель для списка покупок.

    Attributes:
        user (int): id пользователя.
        recipe (int): id рецепта.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Изделие'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return f'{self.user}: {self.item}'
