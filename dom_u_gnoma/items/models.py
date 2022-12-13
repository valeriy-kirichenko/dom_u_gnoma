from typing import Tuple

from django.core.validators import MinValueValidator
from django.db import models

from .utils import image_directory_path


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
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name: str = 'Изделие'
        verbose_name_plural: str = 'Изделия'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return self.name
