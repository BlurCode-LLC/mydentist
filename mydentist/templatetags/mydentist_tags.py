from datetime import timedelta
from django.conf import settings
from django.template import Library
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext_lazy as _
from appointment.models import Appointment
from dentist.models import Service, User_translation, Service_translation
from illness.models import Allergy, Medications, Pregnancy
from mydentist.var import *

register = Library()


@register.simple_tag
def convert_time(minutes):
    time = ""
    language = get_language()
    if language == "uz":
        if minutes // 60 != 0:
            time += f"{str(minutes // 60)} soat"
        if minutes % 60 != 0:
            time += f"{str(minutes % 60)} daqiqa"
    elif language == "ru":
        if minutes // 60 != 0:
            time += f"{str(minutes // 60)} час"
        if minutes % 60 != 0:
            time += f"{str(minutes % 60)} минут"
    return time


@register.simple_tag
def date_format(datetime):
    return f"{datetime.day} {MONTHS[datetime.month - 1]} {datetime.year}"


@register.simple_tag
def time_format(datetime):
    return f"{datetime.hour}:{datetime.minute:02d}"


@register.simple_tag
def last_visit_format(datetime):
    if datetime and datetime != "-":
        now = timezone.now() + timedelta(seconds=settings.TIME_ZONE_HOUR * 3600)
        if now.day == 1 and datetime.day in [28, 29, 30, 31] or now.day - datetime.day == 1:
            return _("kecha")
        else:
            td = now - datetime
            return f"{td.days} {_('kun avval')}"
    return datetime


@register.simple_tag
def get_gender(gender_id):
    return GENDERS[gender_id - 1]


@register.simple_tag
def get_option(select, index):
    options = CHOICES[select]
    if select == "allergy" and index != 1:
        return Allergy.objects.get(pk=index).desc
    elif select == "medications" and index != 1:
        return Medications.objects.get(pk=index).desc
    elif select == "pregnancy" and index != 1:
        return f"{Pregnancy.objects.get(pk=index).desc}-{_('oy')}"
    else:
        for option in options:
            if int(option[0]) == index:
                if select == "anesthesia" and index in [1, 2]:
                    return f"{option[1]} {_('marta')}"
                else:
                    return option[1]
        return None


@register.simple_tag
def get_message(notification):
    # if notification.type == "query":
    #     messages = notification.message.split(NEW_LINE)
    #     message = f"{_('Sabab')}: {messages[0]}{NEW_LINE}{_('Izohlar')}: {messages[1]}"
    # elif notification.type == "appointment":
    #     messages = notification.message.split(NEW_LINE)
    #     print(get_language())
    #     dentist = User_translation.objects.get(
    #         dentist__pk=int(messages[1]),
    #         language__name=get_language()
    #     )
    #     print(messages[0], get_language())
    #     service = Service_translation.objects.get(
    #         service__name=messages[0],
    #         service__dentist__pk=int(messages[1]),
    #         language__name=get_language()
    #     )
    #     appointment = Appointment.objects.get(
    #         dentist__pk=dentist.dentist_id,
    #         service__pk=service.service_id
    #     )
    #     begin_time = f"{date_format(appointment.begin)} {time_format(appointment.begin)}"
    #     end_time = f"{date_format(appointment.end)} {time_format(appointment.end)}"
    #     message = f"{_('Shifokor')}: {dentist.fullname}{NEW_LINE}{_('Xizmat turi')}: {service.name}{NEW_LINE}{_('Boshlanish vaqti')}: {begin_time}{NEW_LINE}{_('Tugash vaqti')}: {end_time}"
    # else:
    #     message = notification.message
    message = notification.message
    return mark_safe(message)
