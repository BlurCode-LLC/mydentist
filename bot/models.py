from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):

    name = models.CharField(_("Ism"), max_length=255)
    lastname = models.CharField(_("Ism"), max_length=255)
    tg_user_id = models.CharField(_("Telegram ID"), max_length=25)
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Til"), on_delete=models.CASCADE, related_name="language_tg_user", default=1)
    status = models.CharField(_("Status (qaysi sahifadaligi)"), max_length=100, default="mainmenu")
    current_page = models.IntegerField(_("Nechinchi sahifada"), default=0)
    latitude = models.FloatField(_("Kenglik"), default=0)
    longitude = models.FloatField(_("Uzunlik"), default=0)

    class Meta:
        verbose_name = _("Telegram foydalanuvchisi")
        verbose_name_plural = _("Telegram foydalanuvchilari")

    def __str__(self):
        return f"{self.name} {self.lastname} - {self.tg_user_id}"
