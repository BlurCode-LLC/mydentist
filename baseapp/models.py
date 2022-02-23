from django.db import models
from django.utils.translation import ugettext_lazy as _


class Language(models.Model):

    name = models.CharField(_("Til nomi"), max_length=25)

    class Meta:
        verbose_name = _("Til")
        verbose_name_plural = _("Tillar")

    def __str__(self):
        return self.name


class Region(models.Model):

    name = models.CharField(_("Hudud nomi"), max_length=50)

    class Meta:
        verbose_name = _("Hudud nomi")
        verbose_name_plural = _("Hudud nomlari")

    def __str__(self):
        return self.name


class Gender(models.Model):

    name = models.CharField(_("Jins"), max_length=20)

    class Meta:
        verbose_name = _("Jins")
        verbose_name_plural = _("Jinslar")

    def __str__(self):
        return self.name
