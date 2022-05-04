from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LoginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "login"
    verbose_name = _("Kirish ma'lumotlari")
