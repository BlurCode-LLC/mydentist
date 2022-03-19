from datetime import date, timedelta
from django.conf import settings as global_settings
from django.contrib.auth import authenticate
from django.db.models import Count
from django.http import JsonResponse
from django.utils import translation, timezone
from django.views.decorators.csrf import csrf_exempt
from json import loads
from appointment.models import Appointment, Query

from dentist.models import Cabinet_Image, User as DentistUser, Patient, Reason, Service_translation
from mydentist.var import ILLNESSES, NEW_LINE, REGIONS
from mydentist.handler import get_results, sort_by_distance, token_encode, token_decode_expired, token_required
from notification.models import Patient2dentist
from patient.models import User as PatientUser


@csrf_exempt
def index(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            services_obj = Service_translation.objects.filter(
                language__name=language
            ).values('name').annotate(
                name_count=Count('name')
            )
            services = []
            for i in range(len(services_obj)):
                services.append({
                    'value': services_obj[i]['name'],
                    'name': services_obj[i]['name'],
                })
            illnesses = {}
            for key, value in ILLNESSES.items():
                illnesses[key] = [{
                    'value': val[0],
                    'name': val[1]
                } for val in value]
            return JsonResponse({
                'services': services,
                'regions': REGIONS,
                'illnesses': illnesses
            })
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def results(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            region = body.get('region')
            service = body.get("service")
            is_woman = body.get('woman')
            hour_24 = body.get("hour_24")
            no_que = body.get("no_que")
            sort_by = body.get("sort_by")
            result = []
            if is_woman and hour_24 and no_que:
                today = date.today()
                services_obj = [service.id for service in Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__gender__pk=2,
                    service__dentist__is_fullday=True
                ) if len(service.service.dentist.dentist_appointment.filter(
                    begin__day=today.day,
                    begin__month=today.month,
                    begin__year=today.year
                )) == 0]
            if is_woman and no_que:
                today = date.today()
                services_obj = [service.id for service in Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__gender__pk=2
                ) if len(service.service.dentist.dentist_appointment.filter(
                    begin__day=today.day,
                    begin__month=today.month,
                    begin__year=today.year
                )) == 0]
            if hour_24 and no_que:
                today = date.today()
                services_obj = [service.id for service in Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__is_fullday=True
                ) if len(service.service.dentist.dentist_appointment.filter(
                    begin__day=today.day,
                    begin__month=today.month,
                    begin__year=today.year
                )) == 0]
            if is_woman and hour_24:
                services_obj = Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__gender__pk=2,
                    service__dentist__is_fullday=True
                )
            if hour_24:
                services_obj = Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__is_fullday=True
                )
            if is_woman:
                services_obj = Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                    service__dentist__gender__pk=2
                )
            if no_que:
                today = date.today()
                services_obj = [service.id for service in Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language
                ) if len(service.service.dentist.dentist_appointment.filter(
                    begin__day=today.day,
                    begin__month=today.month,
                    begin__year=today.year
                )) == 0]
                services_obj = Service_translation.objects.filter(pk__in=services_obj)
            else:
                services_obj = Service_translation.objects.filter(
                    name=service,
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language,
                )
            if sort_by == "price":
                result += get_results(list(services_obj.order_by('service__price')))
            elif sort_by == "near":
                latitude = body.get("lat")
                longitude = body.get("long")
                result += get_results(
                    sort_by_distance(
                        list(services_obj),
                        (
                            float(latitude),
                            float(longitude)
                        )
                    ) if latitude and longitude else list(services_obj)
                )
            return JsonResponse({
                'dentists': result
            })
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def dentist(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            dentist_slug = body.get("slug")
            result = Service_translation.objects.filter(
                service__dentist__slug=dentist_slug,
                language__name=language
            ).first()
            return JsonResponse({
                "fullname": result.service.dentist.dentist_user_translation.filter(language__name=language).first().fullname,
                'image': result.service.dentist.image.url,
                "phone_number": result.service.dentist.phone_number,
                "speciality": result.service.dentist.dentist_user_translation.filter(language__name=language).first().speciality,
                "clinic_name": result.service.dentist.clinic.dentist_clinic_translation.filter(language__name=language).first().name,
                "address": result.service.dentist.clinic.dentist_clinic_translation.filter(language__name=language).first().address,
                "orientir": result.service.dentist.clinic.dentist_clinic_translation.filter(language__name=language).first().orientir,
                "latitude": result.service.dentist.clinic.latitude,
                "longitude": result.service.dentist.clinic.longitude,
                "worktime_begin": result.service.dentist.worktime_begin.strftime("%H:%M"),
                "worktime_end": result.service.dentist.worktime_end.strftime("%H:%M"),
                "services": [{
                    'name': service.dentist_service_translation.filter(language__name=language).first().name,
                    'price': service.price,
                    'duration': service.duration,
                } for service in result.service.dentist.dentist_service.all()],
                'cabinet_images': [ cab.image.url for cab in Cabinet_Image.objects.filter(dentist=result.service.dentist) ],
                'reasons': [{
                    'value': reason.value,
                    'name': reason.name,
                } for reason in Reason.objects.filter(language__name=language)]
            })
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
@token_required
def query(request, user):
    if request.method == "POST":
        if request.body:
            patient = PatientUser.objects.filter(user=user).first()
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            reason = body.get('reason')
            if reason == 25:
                reason = body.get('reason_detail')
            else:
                reason = Reason.objects.filter(
                    value=int(reason),
                    language__name=language
                ).first().name
            comment = body.get('comment')
            dentist_slug = body.get("slug")
            dentist = DentistUser.objects.filter(slug=dentist_slug).first()
            query = Query.objects.create(
                dentist=dentist,
                patient=patient,
                reason=reason,
                comment=comment,
            )
            notification = Patient2dentist.objects.create(
                sender=patient,
                recipient=dentist,
                type="query",
                message=f"{reason}{NEW_LINE}{comment}",
                datetime=timezone.now() + timedelta(seconds=global_settings.TIME_ZONE_HOUR * 3600),
                is_read=False
            )
            dp = Patient.objects.create(
                dentist=dentist,
                patient=patient
            )
            return JsonResponse({
                'message': "Success"
            })
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def register(request):
    pass


@csrf_exempt
def token(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            phone = body.get('phone')
            password = body.get('password')
            if phone and password:
                patient = PatientUser.objects.filter(phone_number=phone).first()
                if patient:
                    user = authenticate(
                        request,
                        username=patient.user.username,
                        password=password
                    )
                    if user:
                        token = token_encode({
                            'user_id': user.id
                        })
                        return JsonResponse({
                            'token': token
                        })
                    else:
                        return JsonResponse({
                            'message': "Incorrect phone or password"
                        }, status=401)
                else:
                    return JsonResponse({
                        'message': "No user with given phone number"
                    }, status=401)
            else:
                return JsonResponse({
                    'message': "Phone or password is missing"
                }, status=401)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def refresh(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            token = body.get('token')
            if token:
                data = token_decode_expired(token)
                token = token_encode(data)
                return JsonResponse({
                    'token': token
                })
            else:
                return JsonResponse({
                    'message': "Token is missing"
                }, status=401)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
@token_required
def profile(request, user):
    patient = PatientUser.objects.filter(user=user).first()
    patient_result = {
        'first_name': patient.user.first_name,
        'last_name': patient.user.last_name,
        'birthday': patient.birthday.strftime("%d.%m.%Y"),
        'email': patient.user.email,
        'phone_number': patient.phone_number,
        'address': patient.address,
        'code': patient.patient_user_id.key
    }
    query = Query.objects.filter(patient=patient).first()
    if query:
        return JsonResponse({
            'patient': patient_result,
            'query': {
                'dentist': query.dentist.dentist_user_translation.filter(language=patient.language).first().fullname,
                'reason': query.reason,
                'comment': query.comment,
            }
        })
    appointment = Appointment.objects.filter(patient=patient).first()
    if appointment:
        return JsonResponse({
            'patient': patient_result,
            'appointment': {
                'dentist': appointment.dentist.dentist_user_translation.filter(language=patient.language).first().fullname,
                'status': appointment.status,
                'service': appointment.service.dentist_service_translation.filter(language=patient.language).first().name,
                'begin_date': appointment.begin.strftime("%d.%m.%Y %H:%M"),
                'comment': appointment.comment
            }
        })
    return JsonResponse({
        'patient': patient_result
    })


@csrf_exempt
@token_required
def settings(request, user):
    patient = PatientUser.objects.filter(user=user).first()
    patient_result = {
        'first_name': patient.user.first_name,
        'last_name': patient.user.last_name,
        'gender': patient.gender.name,
        'birthday': patient.birthday.strftime("%d.%m.%Y"),
        'email': patient.user.email,
        'phone_number': patient.phone_number,
        'address': patient.address,
        'language': patient.language.name
    }
    illness = patient.patient_illness
    patient_illness = {
        'diabet': {
            'value': illness.diabet.value,
            'desc': illness.diabet.desc,
        },
        'anesthesia': {
            'value': illness.anesthesia.value,
            'desc': illness.anesthesia.desc,
        },
        'hepatitis': {
            'value': illness.hepatitis.value,
            'desc': illness.hepatitis.desc,
        },
        'aids': {
            'value': illness.aids.value,
            'desc': illness.aids.desc,
        },
        'pressure': {
            'value': illness.pressure.value,
            'desc': illness.pressure.desc,
        },
        'allergy': {
            'value': illness.allergy.value,
            'desc': illness.allergy.desc,
        },
        'asthma': {
            'value': illness.asthma.value,
            'desc': illness.asthma.desc,
        },
        'dizziness': {
            'value': illness.dizziness.value,
            'desc': illness.dizziness.desc,
        }
    }
    otherillness = patient.patient_otherillness
    patient_otherillness = {
        'epilepsy': {
            'value': otherillness.epilepsy.value,
            'desc': otherillness.epilepsy.desc,
        } if otherillness.epilepsy else None,
        'blood_disease': {
            'value': otherillness.blood_disease.value,
            'desc': otherillness.blood_disease.desc,
        } if otherillness.blood_disease else None,
        'medications': {
            'value': otherillness.medications.value,
            'desc': otherillness.medications.desc,
        } if otherillness.medications else None,
        'stroke': {
            'value': otherillness.stroke.value,
            'desc': otherillness.stroke.desc,
        } if otherillness.stroke else None,
        'heart_attack': {
            'value': otherillness.heart_attack.value,
            'desc': otherillness.heart_attack.desc,
        } if otherillness.heart_attack else None,
        'oncologic': {
            'value': otherillness.oncologic.value,
            'desc': otherillness.oncologic.desc,
        } if otherillness.oncologic else None,
        'tuberculosis': {
            'value': otherillness.tuberculosis.value,
            'desc': otherillness.tuberculosis.desc,
        } if otherillness.tuberculosis else None,
        'alcohol': {
            'value': otherillness.alcohol.value,
            'desc': otherillness.alcohol.desc,
        } if otherillness.alcohol else None,
        'pregnancy': {
            'value': otherillness.pregnancy.value,
            'desc': otherillness.pregnancy.desc,
        } if otherillness.pregnancy else None
    }
    return JsonResponse({
        'patient': patient_result,
        'illness': patient_illness,
        'otherillness': patient_otherillness
    })


@csrf_exempt
@token_required
def update(request, user):
    pass
