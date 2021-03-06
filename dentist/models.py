from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from baseapp.models import Language
from dentist.service_handler import service_creator


class Clinic(models.Model):

    name = models.CharField(_("Nomi"), max_length=100)
    region = models.ForeignKey("baseapp.Region", verbose_name=_("Hudud"), on_delete=models.CASCADE, related_name="clinic_region")
    latitude = models.FloatField(_("Kenglik"), blank=True, null=True)
    longitude = models.FloatField(_("Uzunlik"), blank=True, null=True)

    class Meta:
        verbose_name = _("Shifoxona")
        verbose_name_plural = _("Shifoxonalar")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        trans = Clinic_translation.objects.filter(clinic=self)
        if len(trans) == 0:
            clinic_translation_uz = Clinic_translation.objects.create(
                clinic=self,
                name=self.name,
                address="",
                orientir="",
                language=Language.objects.get(name="uz")
            )
            clinic_translation_ru = Clinic_translation.objects.create(
                clinic=self,
                name=self.name,
                address="",
                orientir="",
                language=Language.objects.get(name="ru")
            )
            clinic_translation_en = Clinic_translation.objects.create(
                clinic=self,
                name=self.name,
                address="",
                orientir="",
                language=Language.objects.get(name="en")
            )


class Clinic_translation(models.Model):

    clinic = models.ForeignKey("dentist.Clinic", verbose_name=_("Shifoxona"), on_delete=models.CASCADE, related_name="dentist_clinic_translation")
    name = models.CharField(_("Nomi"), max_length=100)
    address = models.CharField(_("Manzil"), max_length=255)
    orientir = models.CharField(_("Mo'ljal"), max_length=255, blank=True, null=True)
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Til"), on_delete=models.CASCADE, related_name="clinic_language")

    class Meta:
        verbose_name = _("Shifoxonaning ma'lumoti")
        verbose_name_plural = _("Shifoxonaning ma'lumotlari")

    def __str__(self):
        return f"{self.name} - {self.language.name}"


class User(models.Model):

    user = models.OneToOneField("auth.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_user")
    phone_number = models.CharField(_("Telefon raqami"), max_length=100)
    gender = models.ForeignKey("baseapp.Gender", verbose_name=_("Jins"), on_delete=models.CASCADE, related_name="dentist_gender")
    birthday = models.DateField(_("Tug'ilgan sanasi"), auto_now=False, auto_now_add=False)
    image = models.ImageField(_("Rasmi"), upload_to="dentists/photos/", default="dentists/photos/default.png")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="dentist_language")
    experience = models.IntegerField(_("Tajriba"), blank=True, null=True)
    worktime_begin = models.TimeField(_("Ish vaqti boshlanishi"), auto_now=False, auto_now_add=False)
    worktime_end = models.TimeField(_("Ish vaqti tugashi"), auto_now=False, auto_now_add=False)
    work_days = models.IntegerField(_("Ish kunlari soni (6 yoki 7)"))
    is_fullday = models.BooleanField(_("24 soat rejimi"))
    is_queued = models.BooleanField(_("Navbatsiz"), default=False)
    slug = models.CharField(_("Slug"), max_length=255, blank=True, null=True)
    clinic = models.ForeignKey("dentist.Clinic", verbose_name=_("Shifoxona"), on_delete=models.CASCADE, related_name="dentist_clinic")

    class Meta:
        verbose_name = _("Tish shifokori")
        verbose_name_plural = _("Tish shifokorlari")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def save(self, *args, **kwargs):
        name = f"{self.user.last_name} {self.user.first_name}"
        if self.slug is None or self.slug == "":
            self.slug = name.replace(" ", "-").replace("'", "")
        super().save(*args, **kwargs)
        expire = Expire.objects.filter(dentist=self).first()
        if expire is None:
            expire = Expire.objects.create(
                dentist=self,
                expire_date=timezone.now() + timedelta(days=7)
            )
        trans = User_translation.objects.filter(dentist=self)
        if len(trans) == 0:
            user_translation_uz = User_translation.objects.create(
                dentist=self,
                fullname=str(self),
                speciality="",
                language=Language.objects.get(name="uz")
            )
            user_translation_ru = User_translation.objects.create(
                dentist=self,
                fullname=str(self),
                speciality="",
                language=Language.objects.get(name="ru")
            )
            user_translation_en = User_translation.objects.create(
                dentist=self,
                fullname=str(self),
                speciality="",
                language=Language.objects.get(name="en")
            )
        if len(Service.objects.filter(dentist=self)) == 0:
            service_creator(self, Service, Service_category, Service_translation)


class User_translation(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_user_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="dentist_language_translation")
    fullname = models.CharField(_("MyDentist dagi FIShi"), max_length=100)
    speciality = models.CharField(_("Soha"), max_length=500)

    class Meta:
        verbose_name = _("Tish shifokorining ma'lumoti")
        verbose_name_plural = _("Tish shifokorining ma'lumotlari")

    def __str__(self):
        return f"{self.dentist.__str__()} - {self.language.name}"


class Service_category(models.Model):

    name = models.CharField(_("Xizmat turining nomi"), max_length=255)
    
    class Meta:
        verbose_name = _("Xizmat turi")
        verbose_name_plural = _("Xizmat turlari")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        trans = Service_category_translation.objects.filter(service_category=self)
        if len(trans) == 0:
            service_category_translation_uz = Service_category_translation.objects.create(
                service_category=self,
                name=self.name,
                language=Language.objects.get(name="uz")
            )
            service_category_translation_ru = Service_category_translation.objects.create(
                service_category=self,
                name=self.name,
                language=Language.objects.get(name="ru")
            )
            service_category_translation_en = Service_category_translation.objects.create(
                service_category=self,
                name=self.name,
                language=Language.objects.get(name="en")
            )


class Service_category_translation(models.Model):

    name = models.CharField(_("Xizmat turining nomi"), max_length=255)
    service_category = models.ForeignKey("dentist.Service_category", verbose_name=_("Xizmat turi"), on_delete=models.CASCADE, related_name="service_category_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="service_category_language_translation")
    
    class Meta:
        verbose_name = _("Xizmat turi ma'lumoti")
        verbose_name_plural = _("Xizmat turi ma'lumotlari")

    def __str__(self):
        return f"{self.name} - {self.language.name}"


class Service(models.Model):

    name = models.CharField(_("Xizmat nomi"), max_length=100)
    service_category = models.ForeignKey("dentist.Service_category", verbose_name=_("Xizmat turi"), on_delete=models.CASCADE, related_name="service_category_service", blank=True, null=True)
    price = models.IntegerField(_("Xizmat narxi"), blank=True, null=True)
    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_service")
    is_editable = models.BooleanField(_("Nomini o'zgartirish mumkinmi?"), default=True)
    one_tooth = models.BooleanField(_("Bitta tish uchun"), default=False)

    class Meta:
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")

    def __str__(self):
        return f"{self.name} - {self.dentist.__str__()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        trans = Service_translation.objects.filter(service=self)
        if len(trans) == 0:
            service_translation_uz = Service_translation.objects.create(
                service=self,
                name=self.name,
                language=Language.objects.get(name="uz")
            )
            service_translation_ru = Service_translation.objects.create(
                service=self,
                name=self.name,
                language=Language.objects.get(name="ru")
            )
            service_translation_en = Service_translation.objects.create(
                service=self,
                name=self.name,
                language=Language.objects.get(name="en")
            )


class Service_translation(models.Model):

    service = models.ForeignKey("dentist.Service", verbose_name=_("Xizmat"), on_delete=models.CASCADE, related_name="dentist_service_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE, related_name="service_language_translation")
    name = models.CharField(_("Xizmat nomi"), max_length=100)

    class Meta:
        verbose_name = _("Xizmatning ma'lumoti")
        verbose_name_plural = _("Xizmatning ma'lumotlari")

    def __str__(self):
        return f"{self.service.__str__()} - {self.language.name}"


class Cabinet_Image(models.Model):

    image = models.ImageField(_("Rasm"), upload_to="dentists/cabinet_photos/")
    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Kabinet rasmi")
        verbose_name_plural = _("Kabinet rasmlari")

    def __str__(self):
        return f"{self.image.name} - {self.dentist.__str__()}"


class Reminder(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE)
    name = models.CharField(_("Eslatma"), max_length=200)
    category = models.CharField(_("Eslatma turi"), max_length=50)
    is_done = models.BooleanField(_("Bajarilganmi?"))

    class Meta:
        verbose_name = _("Eslatma")
        verbose_name_plural = _("Eslatmalar")

    def __str__(self):
        return f"{self.name} - {self.dentist.__str__()}"


class Reason(models.Model):

    name = models.CharField(_("Sabab nomi"), max_length=100)
    value = models.IntegerField(_("Raqami"))
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Tili"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Sabab ")
        verbose_name_plural = _("Sabablar")
    
    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Tish shifokori"), on_delete=models.CASCADE, related_name="dentist_patient")
    patient = models.ForeignKey("patient.User", verbose_name=_("Bemor"), on_delete=models.CASCADE, related_name="patient_patient")

    class Meta:
        verbose_name = _("Tish shifokorining bemori ")
        verbose_name_plural = _("Tish shifokorining bemorlari")
    
    def __str__(self):
        return f"{self.dentist.__str__()} - {self.patient.__str__()}"


class Expire(models.Model):

    dentist = models.ForeignKey("dentist.User", verbose_name=_("Aktivlangan"), on_delete=models.CASCADE, related_name="dentist_expire")
    expire_date = models.DateTimeField(_("Tugash muddati"), blank=True, null=True)

    class Meta:
        verbose_name = _("Shifokor aktivligi ")
        verbose_name_plural = _("Shifokor aktivliglari")

    def __str__(self):
        return str(self.dentist)
    
    def save(self, *args, **kwargs):
        if self.expire_date is None:
            expiring = Expire.objects.filter(dentist=self.dentist).last()
            if expiring is not None:
                self.expire_date = expiring.expire_date + timedelta(days=30)
            else:
                self.expire_date = datetime.today() + timedelta(days=30)
        super().save(*args, **kwargs)


class Animation(models.Model):
    
    name = models.CharField(_("Animatsiya nomi"), max_length=150)
    file = models.FileField(_("Fayl"), upload_to="animations/")

    class Meta:
        verbose_name = _("Animatsiya ")
        verbose_name_plural = _("Animatsiyalar")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        trans = Animation_translation.objects.filter(animation=self)
        if len(trans) == 0:
            animation_translation_uz = Animation_translation.objects.create(
                animation=self,
                name=self.name,
                language=Language.objects.get(name="uz")
            )
            animation_translation_ru = Animation_translation.objects.create(
                animation=self,
                name=self.name,
                language=Language.objects.get(name="ru")
            )
            animation_translation_en = Animation_translation.objects.create(
                animation=self,
                name=self.name,
                language=Language.objects.get(name="en")
            )


class Animation_translation(models.Model):

    name = models.CharField(_("Animatsiya nomi"), max_length=150)
    animation = models.ForeignKey("dentist.Animation", verbose_name=_("Animatsiya"), on_delete=models.CASCADE, related_name="animation_translation")
    language = models.ForeignKey("baseapp.Language", verbose_name=_("Til"), on_delete=models.CASCADE, related_name="animation_language")

    class Meta:
        verbose_name = _("Animatsiya ma'lumoti ")
        verbose_name_plural = _("Animatsiya ma'lumotlari")
    
    def __str__(self):
        return self.name
