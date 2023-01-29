from django import forms

from .models import OrderMessage


class OrderMessageForm(forms.ModelForm):
    """Модель формы для отправки сообщения по оплате заказа."""

    class Meta:
        model = OrderMessage
        fields = ('text',)
