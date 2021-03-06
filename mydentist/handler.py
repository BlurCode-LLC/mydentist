from datetime import timedelta
from time import time
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import translation, timezone
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from geopy import distance
from jwt import encode, decode

from appointment.models import Appointment
from baseapp.models import Language
from dentist.models import Expire, Patient, User as DentistUser, User_translation, Clinic, Clinic_translation, Service, Service_translation
from notification.models import *
from patient.models import Payment, User as PatientUser
from .var import CHOICES, GENDERS, NEW_LINE


def set_language(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect("baseapp:index")


def is_authenticated(request, status):
    if request.user.username in request.session:
        if status == "dentist":
            try:
                user = DentistUser.objects.get(user__username=request.user.username)
                expire = Expire.objects.filter(dentist=user).order_by('-id').first()
                print(timezone.now() < expire.expire_date)
                if timezone.now() < expire.expire_date:
                    return True
                return False
            except:
                return False
        elif status == "patient":
            try:
                user = PatientUser.objects.get(user__username=request.user.username)
                return True
            except:
                return False
    else:
        return False


def check_language(request, status):
    if status == "dentist":
        dentist = DentistUser.objects.get(user__username=request.user.username)
        language = Language.objects.get(pk=dentist.language_id).name
        if translation.get_language() != language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
    elif status == "patient":
        patient = PatientUser.objects.get(user__username=request.user.username)
        language = Language.objects.get(pk=patient.language_id).name
        if translation.get_language() != language:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language


def get_queries(queries):
    results = []
    for query in queries:
        dentist_extra = DentistUser.objects.get(pk=query.dentist_id)
        results.append({
            'dentist': User.objects.get(pk=dentist_extra.user_id),
            'dentist_extra': dentist_extra,
            'patient': PatientUser.objects.get(pk=query.patient_id),
            'query': query
        })
    return results


def get_appointments(appointments):
    results = []
    for appointment in appointments:
        dentist_extra = DentistUser.objects.get(pk=appointment.dentist_id)
        results.append({
            'dentist': User.objects.get(pk=dentist_extra.user_id),
            'dentist_extra': dentist_extra,
            'patient': PatientUser.objects.get(pk=appointment.patient_id),
            'services': [Service_translation.objects.filter(
                service__pk=procedure.service_id,
                language__pk=dentist_extra.language_id
            ).first() for procedure in appointment.appointment_procedure.all()],
            'appointment': appointment
        })
    return results


def get_reminders(reminders):
    results = []
    for reminder in reminders:
        results.append({
            'id': reminder.id,
            'name': reminder.name,
            'category': reminder.category,
            'is_done': reminder.is_done
        })
    return results


def sort_by_distance(services, location, priced=False):
    if priced:
        if len(services) < 2:
            return services
        else:
            middle = services[0]
            less = []
            greater = []
            for service in services[1:]:
                dentist = DentistUser.objects.get(pk=service.service.dentist_id)
                service_category = service.service.service_category
                services_obj = list(Service.objects.filter(service_category=service_category, dentist=dentist).order_by("price"))
                price_m = middle.service.price
                if services_obj[0].price < price_m:
                    less.append(service)
                elif services_obj[0].price > price_m:
                    greater.append(service)
                elif services_obj[0].price == price_m:
                    if distance.distance(
                        (
                            service.service.dentist.clinic.latitude,
                            service.service.dentist.clinic.longitude,
                        ),
                        location
                    ).km <= distance.distance(
                        (
                            middle.service.dentist.clinic.latitude,
                            middle.service.dentist.clinic.longitude,
                        ),
                        location
                    ).km:
                        less.append(service)
                    else:
                        greater.append(service)
            return sort_by_distance(less, location, priced=True) + [middle] + sort_by_distance(greater, location, priced=True)
    else:
        if len(services) < 2:
            return services
        else:
            middle = services[0]
            less = []
            greater = []
            for service in services[1:]:
                if distance.distance(
                    (
                        service.service.dentist.clinic.latitude,
                        service.service.dentist.clinic.longitude,
                    ),
                    location
                ).km <= distance.distance(
                    (
                        middle.service.dentist.clinic.latitude,
                        middle.service.dentist.clinic.longitude,
                    ),
                    location
                ).km:
                    less.append(service)
                else:
                    greater.append(service)
            return sort_by_distance(less, location) + [middle] + sort_by_distance(greater, location)


def get_results(services_obj, location):
    results = []
    ids = []
    services = []
    for service_obj in services_obj:
        did = service_obj.service.dentist_id
        if did not in ids:
            ids.append(did)
            services.append(service_obj)
    services = sort_by_distance(services, location, priced=True)
    for service_obj in services:
        dentist = DentistUser.objects.get(pk=service_obj.service.dentist_id)
        expire = Expire.objects.filter(dentist=dentist).order_by('-id').first()
        if timezone.now() < expire.expire_date:
            dentist_extra = User_translation.objects.filter(dentist=dentist, language__pk=service_obj.language_id)[0]
            clinic = Clinic.objects.get(pk=dentist.clinic_id)
            clinic_extra = Clinic_translation.objects.filter(clinic=clinic, language__pk=service_obj.language_id)[0]
            dist = distance.distance((clinic.latitude, clinic.longitude), location).km
            worktime_begin = dentist.worktime_begin
            worktime_end = dentist.worktime_end
            service_category = service_obj.service.service_category
            service_name = service_category.service_category_translation.get(language=service_obj.language).name
            services = list(Service.objects.filter(service_category=service_category, dentist=dentist).order_by("price"))
            price_min = services[0].price
            price_max = services[-1].price
            results.append({
                'image': dentist.image.url,
                'clinic_name': clinic_extra.name,
                'fullname': dentist_extra.fullname,
                'address': clinic_extra.address,
                'orientir': clinic_extra.orientir,
                'latitude': clinic.latitude,
                'longitude': clinic.longitude,
                'distance': dist,
                'worktime_begin': f"{worktime_begin.hour}:{worktime_begin.minute:02d}",
                'worktime_end': f"{worktime_end.hour}:{worktime_end.minute:02d}",
                'is_fullday': dentist.is_fullday,
                'phone_number': dentist.phone_number,
                'service_name': service_name,
                'service_price_min': price_min,
                'service_price_max': price_max,
                'slug': dentist.slug,
            })
        else:
            continue
    return results


def compare_time(datetime, appointments):
    for appointment in appointments:
        if datetime - appointment.begin >= timedelta() and appointment.end - datetime > timedelta():
            if datetime - appointment.begin == timedelta():
                patient = PatientUser.objects.get(pk=appointment.patient_id)
                service = Service_translation.objects.filter(
                    service__pk=appointment.service_id,
                    language__pk=DentistUser.objects.get(
                        pk=appointment.dentist_id).language_id
                )[0]
                duration = appointment.end - appointment.begin
                minutes = duration.seconds // 60
                return f"<td class=\"appointment\" rowspan=\"{minutes // 30}\"><div>{patient}<br>{service.name}</div></td>"
            else:
                return "<td class=\"d-none\"></td>"
    return f"<td class=\"time\">{datetime.strftime('%H:%M')}</td>"


def test_compare_time(datetime, appointments):
    for appointment in appointments:
        if datetime - appointment.begin >= timedelta() and appointment.end - datetime > timedelta():
            if datetime - appointment.begin == timedelta():
                patient = PatientUser.objects.get(pk=appointment.patient_id)
                duration = appointment.end - appointment.begin
                minutes = duration.seconds // 60
                return {
                    'class': "appointment",
                    'rowspan': minutes // 30,
                    'name': f"{patient}<br>{appointment.begin.strftime('%H:%M')} - {appointment.end.strftime('%H:%M')}",
                }
            else:
                return {
                    'class': "d-none",
                    'name': ""
                }
    return {
        'class': "time",
        'name': datetime.strftime('%H:%M')
    }


def compare_appointment(begin, end, appointments):
    for appointment in appointments:
        if begin - appointment.begin >= timedelta():
            if not begin - appointment.end >= timedelta():
                return False
        elif not appointment.begin - end >= timedelta():
            return False
    return True


def get_services(services, language_id):
    results = []
    for service in services:
        results.append({
            'service': service,
            'service_name': Service_translation.objects.filter(
                service=service,
                language__pk=language_id
            )[0]
        })
    return results


def get_option(select, index):
    options = CHOICES[select]
    for option in options:
        if int(option[0]) == index:
            return option[1]
    return None


def get_notifications(request, status):
    # if status == "patient":
    #     notifications_obj = list(Notification.objects.all())[::-1]
    #     notifications = []
    #     for notification_obj in notifications_obj:
    #         notifications.append({
    #             'sender': DentistUser.objects.get(pk=notification_obj.sender_id),
    #             'recipient': PatientUser.objects.get(pk=notification_obj.recipient_id),
    #             'notification': notification_obj
    #         })
    #     return notifications
    # elif status == "dentist":
    #     notifications_obj = list(Notification.objects.all())[::-1]
    #     notifications = []
    #     for notification_obj in notifications_obj:
    #         notifications.append({
    #             'sender': PatientUser.objects.get(pk=notification_obj.sender_id),
    #             'recipient': DentistUser.objects.get(pk=notification_obj.recipient_id),
    #             'notification': notification_obj
    #         })
    #     return notifications
    notifications_obj = list(Notification.objects.all())[::-1]
    notifications = []
    for notification_obj in notifications_obj:
        notifications.append({
            'sender': "MyDentist",
            'notification': notification_obj
        })
    return notifications


def get_patients(request, sort_by):
    patients = [ PatientUser.objects.get(pk=patient.patient_id) for patient in Patient.objects.filter(dentist__user=request.user) ]
    results = []
    for patient in patients:
        appointments = Appointment.objects.filter(
            patient=patient
        ).order_by("begin")
        procedures = []
        for appointment in appointments:
            for procedure in appointment.appointment_procedure.all():
                procedures.append(procedure)
        done = mark_safe(f", {NEW_LINE}".join([ Service_translation.objects.get(
            service=procedure.service,
            language__name=get_language()
        ).name for procedure in procedures if procedure.is_done]))
        total_sum = patient.total
        for payment in Payment.objects.filter(patient=patient):
            total_sum -= payment.sum
        coming = mark_safe(f", {NEW_LINE}".join([ Service_translation.objects.get(
            service=procedure.service,
            language__name=get_language()
        ).name for procedure in procedures if not procedure.is_done]))
        last = appointments.filter(status="done").order_by("-begin").first()
        last_visit = last.begin if last else None
        results.append({
            'patient': User.objects.get(pk=patient.user_id),
            'patient_extra': patient,
            'gender': GENDERS[patient.gender_id - 1],
            'done': done if done != "" else None,
            'total_sum': total_sum,
            'coming': coming if coming != "" else "-",
            'last_visit': last_visit,
        })
    if sort_by is not None:
        if sort_by.split("-")[0] == "debt":
            results = sort_patients(results, "debt")
            if sort_by.split("-")[1] == "down":
                results = results[::-1]
        elif sort_by.split("-")[0] == "plan":
            if "-".join(sort_by.split("-")[1:]) == "done":
                results = [item for item in results if item['done'] is not None]
            elif "-".join(sort_by.split("-")[1:]) == "not-done":
                results = [item for item in results if item['done'] is None]
            else:
                results = results
        elif sort_by.split("-")[0] == "sex":
            if sort_by.split("-")[1] == "male":
                results = [item for item in results if item['gender'] in ["Erkak", "??????????????"]]
            elif sort_by.split("-")[1] == "female":
                results = [item for item in results if item['gender'] in ["Ayol", "??????????????"]]
            else:
                results = results
        elif sort_by.split("-")[0] == "last":
            if "-".join(sort_by.split("-")[1:]) == "yesterday":
                results = [item for item in results if item['last_visit'] and item['last_visit'].day - timezone.now().day in [1, -30, -29, -28, -27]]
            elif "-".join(sort_by.split("-")[1:]) == "this-week":
                results = [item for item in results if item['last_visit'] and item['last_visit'].day - timezone.now().day in [7, -24, -23, -22, -21]]
            elif "-".join(sort_by.split("-")[1:]) == "this-month":
                results = [item for item in results if item['last_visit'] and item['last_visit'].month == timezone.now().month]
            else:
                results = results
        else:
            return 
    return results


def sort_patients(array, sort_by):
    if sort_by == "debt":
        if len(array) < 2:
            return array
        else:
            middle = array[0]
            less = [item for item in array[1:] if item['total_sum'] <= middle['total_sum']]
            greater = [item for item in array[1:] if item['total_sum'] > middle['total_sum']]
            return sort_patients(less, sort_by) + [middle] + sort_patients(greater, sort_by)
    else:
        return array


def token_encode(data):
    payload = {}
    for key, value in data.items():
        payload[key] = value
    payload['exp'] = time() + 86400
    return encode(payload, settings.SECRET_KEY)


def token_decode(token):
    payload = decode(token, settings.SECRET_KEY, ["HS256"])
    data = {}
    for key, value in payload.items():
        if key != 'exp':
            data[key] = value
    return data


def token_decode_expired(token):
    payload = decode(token, settings.SECRET_KEY, ["HS256"], options={
        'verify_exp': False
    })
    data = {}
    for key, value in payload.items():
        if key != 'exp':
            data[key] = value
    return data

def token_required(function):
    def wrapper(request, *args, **kwargs):
        if request.headers:
            try:
                token = request.headers.get('Authorization').split(" ")[1]
            except:
                token = request.headers.get('Authorization')
            if token:
                data = token_decode(token)
                user = User.objects.filter(pk=data['user_id']).first()
                return function(request, user, *args, **kwargs)
            else:
                return JsonResponse({
                    'message': "Token is missing"
                }, status=401)
        else:
            return JsonResponse({
                'message': "No data in request.headers"
            }, status=400)
    return wrapper


# def sort_by_distance(dentists, location):
#     if len(dentists) < 2:
#         return dentists
#     else:
#         middle = dentists[0]
#         less = [
#             dentist for dentist in dentists[1:]
#             if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
#         ]
#         greater = [
#             dentist for dentist in dentists[1:]
#             if distance((dentist['latitude'], dentist['longitude']), location).kilometers <= distance((middle['latitude'], middle['longitude']), location).kilometers
#         ]
#         return sort_by_distance(less, location) + [middle] + sort_by_distance(greater, location)


# def get_ip(request):
#     address = request.META.get("HTTP_X_FORWARDED_FOR")
#     return address.split(",")[-1].strip() if address else request.META.get("REMOTE_ADDR")

# old_full_url = request.META.get("HTTP_REFERER", "/")
# old_url = f"/{'/'.join(old_full_url.split('/')[3:])}"
# prefix_exists = False
# for language in settings.EXTRA_LANGUAGES:
#     if f"/{language[0]}/" in old_url:
#         prefix_exists = True
# if not prefix_exists and user_language != settings.LANGUAGE_CODE:
#     new_url = F"/{user_language}{old_url}"
# elif user_language == settings.LANGUAGE_CODE:
#     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", "/")
# else:
#     new_url = old_url.replace(f"/{old_url.split('/')[1]}/", f"/{user_language}/")
# return redirect(new_url)


class LanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if translation.LANGUAGE_SESSION_KEY in request.session and get_language() != request.session[translation.LANGUAGE_SESSION_KEY]:
            translation.activate(request.session[translation.LANGUAGE_SESSION_KEY])
