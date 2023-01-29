from typing import Tuple

from django.core.validators import MinValueValidator
from django.db import models

from .utils import image_directory_path
from orders.models import Order


class Item(models.Model):
    """Модель для изделия.

    Attributes:
        name (CharField): название изделия.
        description (TextField): описание изделия.
        price (DecimalField): цена.
        image (ImageField): картинка.
        weight (IntegerField): вес изделия.
        is_published (BooleanField): опубликовано или нет.
        order (ForeignKey): id заказа.
    """

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
    is_published = models.BooleanField('Опубликовано', default=True)
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='items'
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name: str = 'Изделие'
        verbose_name_plural: str = 'Изделия'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return self.name
