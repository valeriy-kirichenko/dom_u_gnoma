from django.apps import AppConfig
from django.db.models.signals import post_save


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'

    def ready(self):
        from . import models, signals
        post_save.connect(
            signals.order_checked_dispatcher, models.OrderMessage
        )
