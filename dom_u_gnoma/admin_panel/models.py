from django.contrib.auth import get_user_model
from django.db import models

from orders.models import Order


User = get_user_model()


class OrderMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    text = models.TextField('Текст сообщения')
