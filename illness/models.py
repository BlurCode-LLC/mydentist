from django.db import models
from django.utils.translation import ugettext_lazy as _


class Diabet(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Qand kasalligi ")
        verbose_name_plural = _("Qand kasalligi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Anesthesia(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Narkoz ")
        verbose_name_plural = _("Narkoz")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Hepatitis(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Gepatit (B yoki C) ")
        verbose_name_plural = _("Gepatit (B yoki C)")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class AIDS(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("OITS ")
        verbose_name_plural = _("OITS")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Pressure(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Qon bosimi ")
        verbose_name_plural = _("Qon bosimi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Allergy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Allergiya ")
        verbose_name_plural = _("Allergiya")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Asthma(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Bronxial astma ")
        verbose_name_plural = _("Bronxial astma")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Dizziness(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Bosh aylanishi ")
        verbose_name_plural = _("Bosh aylanishi")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Fainting(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Hushdan ketish ")
        verbose_name_plural = _("Hushdan ketish")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Epilepsy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Epilepsiya (tutqanoq) ")
        verbose_name_plural = _("Epilepsiya (tutqanoq)")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Medications(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Doimiy qabul qiladigan dorilar ")
        verbose_name_plural = _("Doimiy qabul qiladigan dorilar")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Stroke(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Insult bo'lganmisiz? ")
        verbose_name_plural = _("Insult bo'lganmisiz?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Heart_attack(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Infarkt bo'lganmisiz? ")
        verbose_name_plural = _("Infarkt bo'lganmisiz?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Oncologic(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Onkologik kasallik (o'sma - рак) ")
        verbose_name_plural = _("Onkologik kasallik (o'sma - рак)")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Tuberculosis(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Tuberkuloz ")
        verbose_name_plural = _("Tuberkuloz")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Alcohol(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Alkogol iste'mol qilasizmi? ")
        verbose_name_plural = _("Alkogol iste'mol qilasizmi?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Pregnancy(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Homiladormisiz? ")
        verbose_name_plural = _("Homiladormisiz?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"


class Breastfeeding(models.Model):

    value = models.SmallIntegerField(_("Qiymat"))
    desc = models.CharField(_("Tavsif"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Emizasizmi? ")
        verbose_name_plural = _("Emizasizmi?")

    def __str__(self):
        return f"{str(self.value)} - {self.desc}"
