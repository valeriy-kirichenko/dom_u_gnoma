from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import List, Tuple


class User(AbstractUser):
    """Модель для пользователей.

        В качестве логина будет использоваться email, поля ('username',
        'first_name') обязательны к заполнению.
        send_messages отвечает за рассылку пользователям сообщений о
        поступлении новых изделий.

    Attributes:
        username (CharField): имя пользователя.
        password (CharField): пароль.
        email (EmailField): электронная почта.
        first_name (CharField): имя.
        last_name (CharField): фамилия.
        send_messages (BooleanField): флаг для рассылки сообщений.
    """

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['username', 'first_name']

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        help_text=('Введите имя пользователя которое'
                   ' будет отображаться на сайте')
    )
    password = models.CharField(
        'Пароль', max_length=254, help_text='Введите пароль'
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254,
        help_text='Введите вашу электронную почту'
    )
    first_name = models.CharField(
        'Имя', max_length=150, help_text='Введите ваше имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите вашу фамилию (не обязательно)',
        blank=True
    )
    send_messages = models.BooleanField(
        'Рассылка',
        default=False,
    )

    class Meta:
        ordering: Tuple[str] = ('id',)
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self):
        """Возвращает строковое представление модели"""

        return self.username
