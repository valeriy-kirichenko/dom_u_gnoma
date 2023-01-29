from datetime import datetime
from typing import Tuple

from django.db import models

from users.models import User


class Order(models.Model):
    """Модель для изделия.

    Attributes:
        user (ForeignKey): id пользователя.
        last_name (CharField): фамилия.
        first_name (CharField): имя.
        middle_name (CharField): отчество.
        city (CharField): город.
        street (CharField): улица.
        house (CharField): дом/корпус/строение.
        postal_code (CharField): почтовый индекс.
        phone (CharField): телефон.
        email (EmailField): электронная почта.
        created (DateTimeField): дата создания заказа.
        payed (BooleanField): статус оплаты заказа.
        checked (BooleanField): статус обработки заказа.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите вашу фамилию'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Введите ваше имя')
    middle_name = models.CharField(
        'Отчество',
        max_length=150,
        help_text='Введите ваше отчество'
    )
    city = models.CharField(
        'Город',
        max_length=150,
        help_text='Введите название вашего города'
    )
    street = models.CharField(
        'Улица',
        max_length=150,
        help_text='Введите название вашей улицы'
    )
    house = models.CharField(
        'Дом/Корпус/Строение',
        max_length=150,
        help_text='Номер Дома/Корпуса/Строения'
    )
    postal_code = models.CharField(
        'Почтовый индекс',
        max_length=6,
        help_text='Введите ваш почтовый индекс'
    )
    phone = models.CharField(
        'Телефон',
        max_length=11,
        help_text='Введите ваш телефон'
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        help_text='Введите вашу электронную почту'
    )
    created = models.DateTimeField('Дата создания', default=datetime.now())
    payed = models.BooleanField(
        'Оплачено',
        default=False,
    )
    checked = models.BooleanField(
        'Проверен',
        default=False,
    )

    class Meta:
        ordering: Tuple[str] = ('-id',)
        verbose_name: str = 'Заказ'
        verbose_name_plural: str = 'Заказы'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return f'{self.id} - {self.user.last_name} {self.user.first_name}'
