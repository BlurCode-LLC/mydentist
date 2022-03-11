from django.db import models
from django.utils.translation import ugettext_lazy as _

from illness.models import *
from .tooth_handler import teeth_creator


class User(models.Model):

    user = models.OneToOneField("auth.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_user")
    phone_number = models.CharField(_("Telefon raqami"), max_length=50, unique=True)
    gender = models.ForeignKey("baseapp.Gender", verbose_name=_("Jins"), on_delete=models.CASCADE, related_name="patient_gender")
    address = models.CharField(_("Manzil"), max_length=255)
    birthday = models.DateField(_("Tug'ilgan sanasi"), auto_now=False, auto_now_add=False)
    image = models.ImageField(_("Rasmi"), upload_to="patients/photos/", default="patients/photos/default.png")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="patient_language")

    class Meta:
        verbose_name = _("Bemor")
        verbose_name_plural = _("Bemorlar")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            illness = Illness.objects.get(patient=self)
        except:
            illness = Illness.objects.create(
                patient=self,
                diabet=Diabet.objects.get(pk=1),
                anesthesia=Anesthesia.objects.get(pk=4),
                hepatitis=Hepatitis.objects.get(pk=1),
                aids=AIDS.objects.get(pk=1),
                pressure=Pressure.objects.get(pk=1),
                allergy=Allergy.objects.get(pk=1),
                asthma=Asthma.objects.get(pk=1),
                dizziness=Dizziness.objects.get(pk=1),
            )
        try:
            other_illness = Other_Illness.objects.get(patient=self)
        except:
            other_illness = Other_Illness.objects.create(
                patient=self,
                epilepsy=Epilepsy.objects.get(pk=1),
                blood_disease=Blood_disease.objects.get(pk=1),
                medications=Medications.objects.get(pk=1),
                stroke=Stroke.objects.get(pk=1),
                heart_attack=Heart_attack.objects.get(pk=1),
                oncologic=Oncologic.objects.get(pk=1),
                tuberculosis=Tuberculosis.objects.get(pk=1),
                alcohol=Alcohol.objects.get(pk=1),
                pregnancy=Pregnancy.objects.get(pk=1),
            )
        if len(Tooth.objects.filter(patient=self)) == 0:
            teeth_creator(self, Tooth, Tooth_status)


class Illness(models.Model):

    patient = models.OneToOneField("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
    diabet = models.ForeignKey("illness.Diabet", verbose_name=_("Qandli diabet"), on_delete=models.CASCADE)
    anesthesia = models.ForeignKey("illness.Anesthesia", verbose_name=_("Narkoz"), on_delete=models.CASCADE)
    hepatitis = models.ForeignKey("illness.Hepatitis", verbose_name=_("Gepatit B"), on_delete=models.CASCADE)
    aids = models.ForeignKey("illness.AIDS", verbose_name=_("OITS"), on_delete=models.CASCADE)
    pressure = models.ForeignKey("illness.Pressure", verbose_name=_("Qon bosimi"), on_delete=models.CASCADE)
    allergy = models.ForeignKey("illness.Allergy", verbose_name=_("Allergiya"), on_delete=models.CASCADE)
    asthma = models.ForeignKey("illness.Asthma", verbose_name=_("Bronxial astma"), on_delete=models.CASCADE)
    dizziness = models.ForeignKey("illness.Dizziness", verbose_name=_("Bosh aylanishi"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Bemor kasalligi")
        verbose_name_plural = _("Bemor kasalliklari")

    def __str__(self):
        return self.patient.__str__()


class Other_Illness(models.Model):

    patient = models.OneToOneField("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE)
    epilepsy = models.ForeignKey("illness.Epilepsy", verbose_name=_("Epilepsiya"), on_delete=models.CASCADE, blank=True, null=True)
    blood_disease = models.ForeignKey("illness.Blood_disease", verbose_name=_("Qon kasali"), on_delete=models.CASCADE, blank=True, null=True)
    medications = models.ForeignKey("illness.Medications", verbose_name=_("Doimiy dorilar"), on_delete=models.CASCADE, blank=True, null=True)
    stroke = models.ForeignKey("illness.Stroke", verbose_name=_("Insultga uchraganmisiz?"), on_delete=models.CASCADE, blank=True, null=True)
    heart_attack = models.ForeignKey("illness.Heart_attack", verbose_name=_("Yurak xurujiga uchraganmisiz?"), on_delete=models.CASCADE, blank=True, null=True)
    oncologic = models.ForeignKey("illness.Oncologic", verbose_name=_("Onkologik kasalliklar"), on_delete=models.CASCADE, blank=True, null=True)
    tuberculosis = models.ForeignKey("illness.Tuberculosis", verbose_name=_("Sil kasalligi"), on_delete=models.CASCADE, blank=True, null=True)
    alcohol = models.ForeignKey("illness.Alcohol", verbose_name=_("Spirtli ichimlik ichasizmi?"), on_delete=models.CASCADE, blank=True, null=True)
    pregnancy = models.ForeignKey("illness.Pregnancy", verbose_name=_("Homiladorlik"), on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _("Bemorning boshqa kasalligi")
        verbose_name_plural = _("Bemorning boshqa kasalliklari")

    def __str__(self):
        return self.patient.__str__()


class Tooth(models.Model):

    code = models.IntegerField(_("Tish raqami"))
    status = models.ForeignKey("patient.Tooth_status", verbose_name=_("Tish holati"), on_delete=models.CASCADE, related_name="patient_tooth_status")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_tooth")
    comment = models.CharField(_("Izoh"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Tish")
        verbose_name_plural = _("Tishlar")

    def __str__(self):
        return f"{self.code}-{_('tish')} - {self.status} ({self.patient.__str__()})"


class Tooth_status(models.Model):

    name = models.CharField(_("Holat nomi"), max_length=100)
    prefix = models.CharField(_("Holat qo'shimchasi"), max_length=50)

    class Meta:
        verbose_name = _("Tish holati")
        verbose_name_plural = _("Tish holatlari")

    def __str__(self):
        return self.name


class Process_photo(models.Model):
    
    image = models.ImageField(_("Ish jarayonidagi rasm"), upload_to="patients/process_photos/")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_process_photo")

    class Meta:
        verbose_name = _("Davolanish jarayoni")
        verbose_name_plural = _("Davolanish jarayonlari")

    def __str__(self):
        return f"{self.image.name} - {self.patient.__str__()}"


class Key(models.Model):

    patient = models.OneToOneField("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_user_id")
    key = models.IntegerField(_("Kod"))

    class Meta:
        verbose_name = _("Bemor kodi ")
        verbose_name_plural = _("Bemor kodlari")
    
    def __str__(self):
        return f"{self.key} - {self.patient.__str__()}"
