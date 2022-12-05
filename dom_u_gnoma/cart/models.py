from typing import Tuple
from django.db import models

from items.models import Item
from users.models import User


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
        ordering: Tuple[str] = ('-id',)
        verbose_name: str = 'Корзина'
        verbose_name_plural: str = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'item'),
                name='user_item_unique'
            ),
        ]

    def __str__(self):
        """Возвращает строковое представление модели"""

        return f'{self.user}: {self.item}'
