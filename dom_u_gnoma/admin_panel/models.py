from django.contrib.auth import get_user_model
from django.db import models

from orders.models import Order


User = get_user_model()


class OrderMessage(models.Model):
    """Модель для сообщения по оплате заказа.

    Attributes:
        user (ForeignKey): id пользователя.
        order (ForeignKey): id заказа.
        text (TextField): текст сообщения.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    text = models.TextField('Текст сообщения')
