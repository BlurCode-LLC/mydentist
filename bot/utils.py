
from dentist.models import User_translation as DentistUserTranslation


def get_near_dentists(language, tf_hour):
    dentists_translation = DentistUserTranslation.objects.filter(language__name=language)
    result = []
    for dentist_translation in dentists_translation:
        dentist = dentist_translation.dentist
        clinic = dentist.clinic
        clinic_translation = clinic.dentist_clinic_translation.get(language__name=language)
        worktime = f"{dentist.worktime_begin.strftime('%H:%M')} - {dentist.worktime_end.strftime('%H:%M')}" if dentist.is_fullday else tf_hour
        result.append({
            'fullname': dentist_translation.fullname,
            'worktime': worktime,
            'phone_number': dentist.fullname,
            'tg_href': f"https://mydentist.uz/dentist/{dentist.slug}",
            'clinic_name': clinic_translation.name,
            'address': clinic_translation.address,
            'orientir': clinic_translation.orientir if clinic_translation.orientir is not None else "",
            'latitude': clinic.latitude,
            'longitude': clinic.longitude
        })
    return result


def get_location(user):
    return {
        'latitude': user.latitude,
        'longitude': user.longitude
    }


def get_dentists_by_price(status, language):
    pass
