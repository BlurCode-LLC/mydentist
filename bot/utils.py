from dentist.models import Service_category_translation, Service_translation, User_translation as DentistUserTranslation


def get_categories(language):
    [category.name for category in Service_category_translation.objects.filter(language__name=language)]


def get_category(status, language):
    service_category = Service_translation.objects.get(name=status, language__name=language).service.service_category.service_category_translation.filter(language__name=language)
    return service_category.name


def get_services(language, status):
    return [service.name for service in Service_translation.objects.filter(language__name=language, service__service_category__pk=Service_category_translation.objects.get(name=status).service_category_id).distinct("name")]


def get_services_all(language):
    return [service.name for service in Service_translation.objects.filter(language__name=language).distinct("name")]


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


def get_dentists_by_price(status, language):
    pass


def get_location(user):
    return {
        'latitude': user.latitude,
        'longitude': user.longitude
    }


def get_24_7_dentists(language, tf_hour):
    dentists_translation = DentistUserTranslation.objects.filter(language__name=language, is_fullday=True)
    result = []
    for dentist_translation in dentists_translation:
        dentist = dentist_translation.dentist
        clinic = dentist.clinic
        clinic_translation = clinic.dentist_clinic_translation.get(language__name=language)
        result.append({
            'fullname': dentist_translation.fullname,
            'worktime': tf_hour,
            'phone_number': dentist.fullname,
            'tg_href': f"https://mydentist.uz/dentist/{dentist.slug}",
            'clinic_name': clinic_translation.name,
            'address': clinic_translation.address,
            'orientir': clinic_translation.orientir if clinic_translation.orientir is not None else "",
            'latitude': clinic.latitude,
            'longitude': clinic.longitude
        })
    return result


def location_not_exists(user):
    return user.latitude == 0 and user.longitude == 0
