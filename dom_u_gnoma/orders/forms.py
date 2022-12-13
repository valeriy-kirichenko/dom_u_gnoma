from django import forms

from .models import Order


class OrderCreationForm(forms.ModelForm):
    policy = forms.BooleanField(
        label='',
        required=True,
        help_text=('Я даю свое согласие на обработку персональных данных'
                   ' на условиях, определенных '
                   '<a href={% url "" %} target="_blank">'
                   'Политикой конфиденциальности</a>'),
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Order
        fields = (
            'last_name',
            'first_name',
            'middle_name',
            'city',
            'street',
            'house',
            'postal_code',
            'email',
            'phone',
            'policy',
        )
