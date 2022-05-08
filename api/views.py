from datetime import date, datetime, timedelta
from random import randint
from django.conf import settings as global_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.utils import translation, timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from json import loads

from appointment.models import Appointment, Query
from baseapp.models import Gender, Language
from dentist.models import Cabinet_Image, Service_category_translation, User as DentistUser, Patient, Reason, Service_translation
from illness.models import *
from login.models import PasswordReset
from login.tokens import reset_password_token
from mydentist.var import ILLNESSES, NEW_LINE, REGIONS
from mydentist.handler import get_results, sort_by_distance, token_encode, token_decode_expired, token_required
from notification.models import Dentist2patient, Patient2dentist
from patient.models import Illness, Key, Other_Illness, User as PatientUser


@csrf_exempt
def index(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            services = [{
                'value': item.service_category_id,
                'name': item.name
            } for item in Service_category_translation.objects.filter(language__name=language).order_by("id")]
            regions = []
            for region in REGIONS:
                regions.append({
                    'value': region['value'],
                    'name': region['name'],
                    'has_dentists': True if len(DentistUser.objects.filter(clinic__region__pk=region['value'])) else False,
                })
            illnesses = {}
            for key, value in ILLNESSES.items():
                illnesses[key] = [{
                    'value': "0",
                    'name': _("Tanlang")
                }]
                for val in value:
                    illnesses[key].append({
                        'value': val[0],
                        'name': val[1]
                    })
            return JsonResponse({
                'services': services,
                'regions': regions,
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
            def searcher():
                if is_woman and hour_24 and no_que:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        language__name=language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True,
                        service__dentist__is_queued=True
                    )
                elif is_woman and no_que:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        language__name=language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_queued=True
                    )
                elif hour_24 and no_que:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        language__name=language,
                        service__dentist__is_fullday=True,
                        service__dentist__is_queued=True
                    )
                elif is_woman and hour_24:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        language__name=language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True
                    )
                elif hour_24:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        service__dentist__is_fullday=True,
                        language__name=language
                    )
                elif is_woman:
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        service__dentist__gender__pk=2,
                        language__name=language
                    )
                elif no_que:
                    today = date.today()
                    return Service_translation.objects.filter(
                        service__service_category__pk=int(service),
                        service__dentist__clinic__region__pk=int(region),
                        language__name=language,
                        service__dentist__is_queued=True
                    )
                return Service_translation.objects.filter(
                    service__service_category__pk=int(service),
                    service__dentist__clinic__region__pk=int(region),
                    language__name=language
                )
            services_obj = searcher()
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
            reason = body.get('reason').split(", ")
            comment = body.get('comment')
            dentist_slug = body.get("slug")
            dentist = DentistUser.objects.filter(slug=dentist_slug).first()
            new_reason = []
            for r in reason:
                try:
                    temp = Reason.objects.get(
                        name=r,
                        language=patient.language
                    )
                    new = Reason.objects.get(
                        value=temp.value,
                        language=dentist.language
                    )
                    new_reason.append(new.name)
                except:
                    new_reason.append(r)
            query = Query.objects.create(
                dentist=dentist,
                patient=patient,
                reason=", ".join(new_reason),
                comment=comment,
            )
            notification = Patient2dentist.objects.create(
                sender=patient,
                recipient=dentist,
                type="query",
                message=f"{', '.join(new_reason)}{NEW_LINE}{comment}",
                datetime=timezone.now() + timedelta(seconds=global_settings.TIME_ZONE_HOUR * 3600),
                is_read=False
            )
            dp = Patient.objects.get_or_create(
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
def register_user(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            language = body.get('language') or "uz"
            file_path = global_settings.PROJECT_DIR / "last_id.txt"
            with open(file_path, "r") as file:
                id = int(file.read()) + 1
            with open(file_path, "w") as file:
                file.write(str(id))
            id = f"{id:07d}"
            password = body.get('password')
            password_confirm = body.get('password_confirm')
            if password != password_confirm:
                return JsonResponse({
                    'message': "Passwords do not match"
                })
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            phone = body.get('phone')
            email = body.get('email') or ""
            if PatientUser.objects.filter(phone_number=phone).first():
                return JsonResponse({
                    'message': "User with this phone number already exists"
                })
            address = body.get('address')
            birthday = body.get('birthday')
            birthday = datetime.strptime(birthday, "%d-%m-%Y")
            gender = body.get('gender')
            new_user = User.objects.create_user(
                f"user{id}",
                password=password,
                last_name=last_name,
                first_name=first_name,
                email=email
            )
            new_patient = PatientUser.objects.create(
                user=new_user,
                phone_number=phone,
                address=address,
                birthday=birthday,
                image="patients/photos/default.png",
                language=Language.objects.get(name=language),
                gender=Gender.objects.get(pk=gender)
            )
            key = Key.objects.create(
                patient=new_patient,
                key=randint(100000, 999999)
            )
            token = token_encode({
                'user_id': new_user.id
            })
            return JsonResponse({
                'token': token
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
def register_illness(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            illness = Illness.objects.filter(patient__phone_number=body.get('phone')).first()
            if illness:
                illness.diabet_id = Diabet.objects.get(value=int(body.get('diabet'))).id
                illness.anesthesia_id = Anesthesia.objects.get(value=int(body.get('anesthesia'))).id
                illness.hepatitis_id = Hepatitis.objects.get(value=int(body.get('hepatitis'))).id
                illness.aids_id = AIDS.objects.get(value=int(body.get('aids'))).id
                illness.pressure_id = Pressure.objects.get(value=int(body.get('pressure'))).id
                allergy = int(body.get('allergy'))
                if allergy == 2:
                    allergy_detail = body.get('allergy_detail')
                    try:
                        allergy = Allergy.objects.get(
                            value=allergy,
                            desc=allergy_detail,
                        )
                    except:
                        allergy = Allergy.objects.create(
                            value=allergy,
                            desc=allergy_detail,
                        )
                else:
                    allergy = Allergy.objects.get(
                        value=allergy,
                    )
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=int(body.get('asthma'))).id
                illness.dizziness_id = Dizziness.objects.get(value=int(body.get('dizziness'))).id
                illness.fainting_id = Fainting.objects.get(value=int(body.get('dizziness'))).id
                illness.save()
                return JsonResponse({
                    'message': "Success"
                })
            else:
                return JsonResponse({
                    'message': "No user data in request.body"
                }, status=400)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def register_other_illness(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            otherillness = Other_Illness.objects.get(patient__phone_number=body.get('phone'))
            if otherillness:
                otherillness.epilepsy_id = Epilepsy.objects.get(value=int(body.get('epilepsy'))).id if body.get('epilepsy') is not None else None
                if body.get('medications') is not None:
                    medications = int(body.get('medications'))
                    if medications == 2:
                        medications_detail = body.get('medications_detail')
                        try:
                            medications = Medications.objects.get(
                                value=medications,
                                desc=medications_detail,
                            )
                        except:
                            medications = Medications.objects.create(
                                value=medications,
                                desc=medications_detail,
                            )
                    else:
                        medications = Medications.objects.get(
                            value=medications,
                        )
                    otherillness.medications_id = medications.id
                else:
                    otherillness.medications_id = None
                otherillness.stroke_id = Stroke.objects.get(value=int(body.get('stroke'))).id if body.get('stroke') is not None else None
                otherillness.heart_attack_id = Heart_attack.objects.get(value=int(body.get('heart_attack'))).id if body.get('heart_attack') is not None else None
                otherillness.oncologic_id = Oncologic.objects.get(value=int(body.get('oncologic'))).id if body.get('oncologic') is not None else None
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=int(body.get('tuberculosis'))).id if body.get('tuberculosis') is not None else None
                otherillness.alcohol_id = Alcohol.objects.get(value=int(body.get('alcohol'))).id if body.get('alcohol') is not None else None
                if body.get('pregnancy') is not None:
                    pregnancy = int(body.get('pregnancy'))
                    if pregnancy == 2:
                        pregnancy_detail = body.get('pregnancy_detail')
                        try:
                            pregnancy = Pregnancy.objects.get(
                                value=pregnancy,
                                desc=pregnancy_detail,
                            )
                        except:
                            pregnancy = Pregnancy.objects.create(
                                value=pregnancy,
                                desc=pregnancy_detail,
                            )
                    else:
                        pregnancy = Pregnancy.objects.get(
                            value=pregnancy,
                        )
                    otherillness.pregnancy_id = pregnancy.id
                else:
                    otherillness.pregnancy_id = None
                otherillness.breastfeeding_id = Breastfeeding.objects.get(value=int(body.get('breastfeeding_id'))).id if body.get('breastfeeding_id') is not None else None
                otherillness.save()
                return JsonResponse({
                    'message': "Success"
                })
            else:
                return JsonResponse({
                    'message': "No user data in request.body"
                }, status=400)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


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
        'code': patient.patient_user_id.key,
        'language': patient.language.name,
        'image': patient.image.url
    }
    query = Query.objects.filter(patient=patient).first()
    if query:
        return JsonResponse({
            'patient': patient_result,
            'query': {
                'dentist': query.dentist.dentist_user_translation.filter(language=patient.language).first().fullname,
                'reason': query.reason,
                'comment': query.comment,
            },
            'appointment': None
        })
    appointment = Appointment.objects.filter(patient=patient).first()
    if appointment:
        return JsonResponse({
            'patient': patient_result,
            'query': None,
            'appointment': {
                'dentist': appointment.dentist.dentist_user_translation.filter(language=patient.language).first().fullname,
                'status': appointment.status,
                'service': appointment.service.dentist_service_translation.filter(language=patient.language).first().name,
                'begin_date': appointment.begin.strftime("%d.%m.%Y %H:%M"),
                'comment': appointment.comment
            }
        })
    return JsonResponse({
        'patient': patient_result,
        'query': None,
        'appointment': None
    })


@csrf_exempt
@token_required
def notifications(request, user):
    notifications_obj = list(Dentist2patient.objects.filter(recipient__user=user))[::-1]
    notifications = []
    for notification_obj in notifications_obj:
        notifications.append({
            'sender': str(notification_obj.sender),
            'text': notification_obj.message,
            'datetime': notification_obj.datetime.strftime("%B %d, %Y")
        })
    return JsonResponse(notifications, safe=False)


@csrf_exempt
@token_required
def settings(request, user):
    patient = PatientUser.objects.filter(user=user).first()
    patient_result = {
        'first_name': patient.user.first_name,
        'last_name': patient.user.last_name,
        'gender': patient.gender.id,
        'birthday': patient.birthday.strftime("%d.%m.%Y"),
        'email': patient.user.email,
        'phone_number': patient.phone_number,
        'address': patient.address,
        'language': patient.language.name,
        'image': patient.image.url
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
        },
        'fainting': {
            'value': illness.fainting.value,
            'desc': illness.fainting.desc,
        }
    }
    otherillness = patient.patient_otherillness
    patient_otherillness = {
        'epilepsy': {
            'value': otherillness.epilepsy.value,
            'desc': otherillness.epilepsy.desc,
        } if otherillness.epilepsy else None,
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
        } if otherillness.pregnancy else None,
        'breastfeeding': {
            'value': otherillness.breastfeeding.value,
            'desc': otherillness.breastfeeding.desc,
        } if otherillness.breastfeeding else None
    }
    return JsonResponse({
        'patient': patient_result,
        'illness': patient_illness,
        'otherillness': patient_otherillness
    })


@csrf_exempt
@token_required
def update_user(request, user):
    if request.method == "POST":
        if request.body:
            patient = PatientUser.objects.filter(user=user).first()
            body = loads(request.body.decode("utf-8"))
            first_name = body.get('first_name')
            last_name = body.get('last_name')
            gender = int(body.get('gender'))
            birthday = body.get('birthday')
            birthday = datetime.strptime(birthday, "%d-%m-%Y")
            email = body.get('email')
            phone = body.get('phone')
            address = body.get('address')
            language = body.get('language')
            if user.first_name != first_name:
                user.first_name = first_name
            if user.last_name != last_name:
                user.last_name = last_name
            if user.email != email:
                user.email = email
            if patient.gender_id != gender:
                patient.gender_id = gender
            if datetime.strptime(patient.birthday.strftime("%d-%m-%Y"), "%d-%m-%Y") - birthday != timedelta():
                patient.birthday = birthday
            if patient.phone_number != phone:
                if PatientUser.objects.filter(phone_number=phone).first():
                    return JsonResponse({
                        'message': "User with this phone number already exists"
                    })
                patient.phone_number = phone
            if patient.address != address:
                patient.address = address
            if patient.language.name != language:
                patient.language_id = Language.objects.get(name=language).id
            user.save()
            patient.save()
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
@token_required
def update_password(request, user):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            old_password = body.get('old_password')
            password = body.get('password')
            password_confirm = body.get('password_confirm')
            if authenticate(request, username=user.username, password=old_password) is None:
                return JsonResponse({
                    'message': "Old password is not correct"
                })
            if password != password_confirm:
                return JsonResponse({
                    'message': "Passwords do not match"
                })
            if password == "":
                return JsonResponse({
                    'message': "Password can not be empty"
                })
            user.set_password(password)
            user.save()
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
@token_required
def update_illness(request, user):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            illness = Illness.objects.filter(patient__user=user).first()
            if illness:
                illness.diabet_id = Diabet.objects.get(value=int(body.get('diabet'))).id
                illness.anesthesia_id = Anesthesia.objects.get(value=int(body.get('anesthesia'))).id
                illness.hepatitis_id = Hepatitis.objects.get(value=int(body.get('hepatitis'))).id
                illness.aids_id = AIDS.objects.get(value=int(body.get('aids'))).id
                illness.pressure_id = Pressure.objects.get(value=int(body.get('pressure'))).id
                allergy = int(body.get('allergy'))
                if allergy == 2:
                    allergy_detail = body.get('allergy_detail')
                    try:
                        allergy = Allergy.objects.get(
                            value=allergy,
                            desc=allergy_detail,
                        )
                    except:
                        allergy = Allergy.objects.create(
                            value=allergy,
                            desc=allergy_detail,
                        )
                else:
                    allergy = Allergy.objects.get(
                        value=allergy,
                    )
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=int(body.get('asthma'))).id
                illness.dizziness_id = Dizziness.objects.get(value=int(body.get('dizziness'))).id
                illness.fainting_id = Fainting.objects.get(value=int(body.get('fainting'))).id
                illness.save()
                return JsonResponse({
                    'message': "Success"
                })
            else:
                return JsonResponse({
                    'message': "No user data in request.body"
                }, status=400)
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
def update_other_illness(request, user):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            otherillness = Other_Illness.objects.filter(patient__user=user).first()
            if otherillness:
                otherillness.epilepsy_id = Epilepsy.objects.get(value=int(body.get('epilepsy'))).id if body.get('epilepsy') is not None else None
                if body.get('medications') is not None:
                    medications = int(body.get('medications'))
                    if medications == 2:
                        medications_detail = body.get('medications_detail')
                        try:
                            medications = Medications.objects.get(
                                value=medications,
                                desc=medications_detail,
                            )
                        except:
                            medications = Medications.objects.create(
                                value=medications,
                                desc=medications_detail,
                            )
                    else:
                        medications = Medications.objects.get(
                            value=medications,
                        )
                    otherillness.medications_id = medications.id
                else:
                    otherillness.medications_id = None
                otherillness.stroke_id = Stroke.objects.get(value=int(body.get('stroke'))).id if body.get('stroke') is not None else None
                otherillness.heart_attack_id = Heart_attack.objects.get(value=int(body.get('heart_attack'))).id if body.get('heart_attack') is not None else None
                otherillness.oncologic_id = Oncologic.objects.get(value=int(body.get('oncologic'))).id if body.get('oncologic') is not None else None
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=int(body.get('tuberculosis'))).id if body.get('tuberculosis') is not None else None
                otherillness.alcohol_id = Alcohol.objects.get(value=int(body.get('alcohol'))).id if body.get('alcohol') is not None else None
                if body.get('pregnancy') is not None:
                    pregnancy = int(body.get('pregnancy'))
                    if pregnancy == 2:
                        pregnancy_detail = body.get('pregnancy_detail')
                        try:
                            pregnancy = Pregnancy.objects.get(
                                value=pregnancy,
                                desc=pregnancy_detail,
                            )
                        except:
                            pregnancy = Pregnancy.objects.create(
                                value=pregnancy,
                                desc=pregnancy_detail,
                            )
                    else:
                        pregnancy = Pregnancy.objects.get(
                            value=pregnancy,
                        )
                    otherillness.pregnancy_id = pregnancy.id
                else:
                    otherillness.pregnancy_id = None
                otherillness.breastfeeding_id = Breastfeeding.objects.get(value=int(body.get('breastfeeding'))).id if body.get('breastfeeding') is not None else None
                otherillness.save()
                return JsonResponse({
                    'message': "Success"
                })
            else:
                return JsonResponse({
                    'message': "No user data in request.body"
                }, status=400)
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
def update_photo(request, user):
    if request.method == "POST" and 'file' in request.FILES:
        photo = request.FILES.get("file")
        patient = PatientUser.objects.get(user=user)
        patient.image = photo
        patient.save()
        return JsonResponse({
            'photo': patient.image.url
        }, safe=False)


@csrf_exempt
def password_reset(request):
    if request.method == "POST":
        if request.body:
            body = loads(request.body.decode("utf-8"))
            email = body.get('email')
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    uidb64 = urlsafe_base64_encode(force_bytes(user.username))
                    token = reset_password_token.make_token(user)
                    password_reset = PasswordReset.objects.create(
                        email=email,
                        uidb64=uidb64,
                        token=token,
                        is_active=True
                    )
                    text = f"You're receiving this email because you requested a password reset for your user account at {request.META.get('HTTP_HOST')}.\n\nPlease go to the following page and choose a new password: {request.META.get('HTTP_ORIGIN')}/auth/reset/{uidb64}/{token}\n\nThanks for using our site!"
                    result_email = send_mail(_("Parolni tiklash"), text, global_settings.EMAIL_HOST_USER, [email])
                    if result_email:
                        return JsonResponse({
                            'message': "Success"
                        })
                else:
                    return JsonResponse({
                        'message': "No user with given email"
                    }, status=404)
            else:
                return JsonResponse({
                    'message': "No email provided"
                }, status=400)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)


@csrf_exempt
def reset(request, uidb64, token):
    if request.method == "POST":
        if request.body:
            print(request.body.decode("utf-8"))
            print(request.POST)
            body = loads(request.body.decode("utf-8"))
            user = User.objects.filter(username=force_str(urlsafe_base64_decode(uidb64))).first()
            if user:
                is_token_correct = reset_password_token.check_token(user, token)
                if is_token_correct:
                    password_reset = PasswordReset.objects.filter(
                        email=user.email,
                        uidb64=uidb64,
                        token=token
                    ).first()
                    if password_reset.is_active:
                        password = body.get('password')
                        password_confirm = body.get('password_confirm')
                        if password == password_confirm:
                            user.set_password(password)
                            user.save()
                            password_reset.is_active = False
                            password_reset.save()
                            return JsonResponse({
                                'message': "Success"
                            })
                        else:
                            return JsonResponse({
                                'message': "Passwords do not match"
                            }, status=400)
                    else:
                        return JsonResponse({
                            'message': "Link is invalid"
                        }, status=404)
                else:
                    return JsonResponse({
                        'message': "Token isn't verified"
                    }, status=400)
            else:
                return JsonResponse({
                    'message': "No user with given uidb64"
                }, status=404)
        else:
            return JsonResponse({
                'message': "No data in request.body"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Method not allowed"
        }, status=405)
