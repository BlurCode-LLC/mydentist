from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PatientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "patient"
    verbose_name = _("Bemor ma'lumotlari")
