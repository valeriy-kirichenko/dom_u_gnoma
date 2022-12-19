from django import forms

from .models import OrderMessage


class OrderMessageForm(forms.ModelForm):

    class Meta:
        model = OrderMessage
        fields = ('text',)
