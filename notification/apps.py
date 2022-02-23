from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification"
    verbose_name = _("Xabarlar")
