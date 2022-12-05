from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.dispatch import Signal


user_registered = Signal()


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self):
        from . import signals
        user_registered.connect(signals.user_registered_dispatcher)
        user_logged_in.connect(signals.user_logged_in_dispatcher)
