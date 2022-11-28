from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from .apps import user_registered


User = get_user_model()


class CreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите имя пользователя'}
        ),
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите вашу электронную почту'}
        ),
    )
    send_messages = forms.BooleanField(
        label='Рассылка',
        required=False,
        help_text=('Я хочу получать письма при новых поступлениях изделий'),
        widget=forms.CheckboxInput()
    )
    policy = forms.BooleanField(
        label='',
        required=True,
        help_text=('Я даю свое согласие на обработку персональных данных'
                   ' на условиях, определенных '
                   '<a href={% url "" %}>'
                   'Политикой конфиденциальности</a>'),
        widget=forms.CheckboxInput()
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        user_registered.send(UserCreationForm, instance=user)
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'send_messages',
            'policy',
        )
