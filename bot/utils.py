from dentist.models import Service_category_translation, Service_translation, User_translation as DentistUserTranslation


def get_categories(language):
    return [category.name for category in Service_category_translation.objects.filter(language__name=language)]


def get_category(status, language):
    service_category = Service_translation.objects.filter(name=status, language__name=language).first().service.service_category.service_category_translation.filter(language__name=language).first()
    return service_category.name


def get_services(language, status):
    return [service.name for service in Service_translation.objects.filter(language__name=language, service__service_category__pk=Service_category_translation.objects.get(name=status, language__name=language).service_category_id).distinct("name")]


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
            'phone_number': dentist.phone_number,
            'tg_href': f"https://mydentist.uz/dentist/{dentist.slug}",
            'clinic_name': clinic_translation.name,
            'address': clinic_translation.address,
            'orientir': clinic_translation.orientir if clinic_translation.orientir is not None else "",
            'latitude': clinic.latitude,
            'longitude': clinic.longitude
        })
    return result


def get_dentists_by_price(status, language, tf_hour):
    services_translation = Service_translation.objects.filter(name=status, language__name=language).order_by("service__price")
    result = []
    for service_translation in services_translation:
        service = service_translation.service
        dentist = service_translation.service.dentist
        dentist_translation = dentist.dentist_user_translation.get(language__name=language)
        clinic = dentist.clinic
        clinic_translation = clinic.dentist_clinic_translation.get(language__name=language)
        result.append({
            'service_name': service_translation.name,
            'price': service.price,
            'fullname': dentist_translation.fullname,
            'worktime': f"{dentist.worktime_begin.strftime('%H:%M')} - {dentist.worktime_end.strftime('%H:%M')}" if dentist.is_fullday else tf_hour,
            'phone_number': dentist.phone_number,
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


def get_24_7_dentists(language, tf_hour):
    dentists_translation = DentistUserTranslation.objects.filter(language__name=language, dentist__is_fullday=True)
    # with open("debug.txt", "a") as file:
    #     file.write(", ".join([dentist.name for dentist in dentists_translation]) + "\n")
    result = []
    for dentist_translation in dentists_translation:
        dentist = dentist_translation.dentist
        clinic = dentist.clinic
        clinic_translation = clinic.dentist_clinic_translation.get(language__name=language)
        result.append({
            'fullname': dentist_translation.fullname,
            'worktime': tf_hour,
            'phone_number': dentist.phone_number,
            'tg_href': f"https://mydentist.uz/dentist/{dentist.slug}",
            'clinic_name': clinic_translation.name,
            'address': clinic_translation.address,
            'orientir': clinic_translation.orientir if clinic_translation.orientir is not None else "",
            'latitude': clinic.latitude,
            'longitude': clinic.longitude
        })
    # with open("debug.txt", "a") as file:
    #     file.write(", ".join([dentist['fullname'] for dentist in result]) + "\n")
    return result


def location_not_exists(user):
    return user.latitude == 0 and user.longitude == 0
