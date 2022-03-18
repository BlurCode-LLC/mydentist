from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Query(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
    reason = models.CharField(_("Sabab"), max_length=255)
    comment = models.TextField(_("Izohlar"))

    class Meta:
        verbose_name = _("So'rov")
        verbose_name_plural = _("So'rovlar")

    def __str__(self):
        return f"{self.patient.__str__()} - {self.dentist.__str__()}"


class Appointment(models.Model):
    
    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_appointment")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
    service = models.ForeignKey("dentist.Service", verbose_name=_("Xizmat"), on_delete=models.CASCADE)
    begin = models.DateTimeField(_("Boshlanish vaqti"), default=None, auto_now=False, auto_now_add=False)
    end = models.DateTimeField(_("Tugash vaqti"), default=None, auto_now=False, auto_now_add=False)
    comment = models.TextField(_("Izohlar"), blank=False, null=True)
    status = models.CharField(_("Qabul holati"), max_length=50)

    class Meta:
        verbose_name = _("Qabul")
        verbose_name_plural = _("Qabullar")

    def __str__(self):
        return f"{self.patient.__str__()} - {self.dentist.__str__()}"
    
    def upcoming(self):
        return self.begin >= timezone.now() + timedelta(seconds=settings.TIME_ZONE_HOUR * 3600)
