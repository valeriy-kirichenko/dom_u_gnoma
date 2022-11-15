from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.signing import BadSignature 
from django.views.generic import CreateView, TemplateView
from django.shortcuts import get_object_or_404, render

from django.urls import reverse_lazy

from .forms import CreationForm, User
from .utils import signer


def user_activate(request, sign):
    try:
        username = signer.unsign(sign) 
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_active:
        return render(request, 'users/user_activated.html')
    else:
        user.is_active = True
        user.save()
        return render(request, 'users/activation_done.html')


class RegisterUserView(UserPassesTestMixin, CreateView):
    """View класс для регистрации пользователя."""

    model = User
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:register_done')

    def test_func(self):
        """Проверяет является ли пользователь анонимом.

        Returns:
            bool: True если пользователь аноним иначе False.
        """

        return self.request.user.is_anonymous


class RegisterDoneView(TemplateView):
    """View класс для завершения регистрации пользователя."""

    template_name = 'users/register_done.html'
