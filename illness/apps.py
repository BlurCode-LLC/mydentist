from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IllnessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illness"
    verbose_name = _("Kasalliklar")
