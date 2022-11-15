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
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите ваше настоящее имя'}
        ),
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите вашу фамилию'}
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
        help_text=('Хотите ли вы получать письма о выходе новых изделий на'
                   ' указанную электронную почту?'),
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
            'username', 'first_name', 'last_name', 'email', 'send_messages'
        )
