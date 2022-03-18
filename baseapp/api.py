from datetime import date
from django.db.models import Count
from django.http import JsonResponse
from django.utils import translation
from json import loads

from dentist.models import Service_translation, User as DentistUser
from mydentist.var import REGIONS
from mydentist.handler import get_results, sort_by_distance


# def login(request):
#     body = loads(request.body.decode("utf-8"))
#     phone = body.get('email')
#     password = body.get('password')
#     language = body.get('language')
#     translation.activate(language)
#     request.session[translation.LANGUAGE_SESSION_KEY] = language
    
    

#     return JsonResponse({
#         'services': services,
#         'regions': REGIONS
#     })


def index(request):
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
    return JsonResponse({
        'services': services,
        'regions': REGIONS
    })




def results(request):
    body = loads(request.body.decode("utf-8"))
    language = body.get('language') or "uz"
    region = body.get('region')
    service = body.get("service")
    is_woman = body.get('woman')
    print(is_woman)
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
    elif is_woman and hour_24:
        services_obj = Service_translation.objects.filter(
            name=service,
            service__dentist__clinic__region__pk=int(region),
            language__name=language,
            service__dentist__gender__pk=2,
            service__dentist__is_fullday=True
        )
    elif hour_24:
        services_obj = Service_translation.objects.filter(
            name=service,
            service__dentist__clinic__region__pk=int(region),
            language__name=language,
            service__dentist__is_fullday=True
        )
    elif is_woman:
        services_obj = Service_translation.objects.filter(
            name=service,
            service__dentist__clinic__region__pk=int(region),
            language__name=language,
            service__dentist__gender__pk=2
        )
    elif no_que:
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
        result += get_results(
            sort_by_distance(
                list(services_obj),
                (
                    # geoform.cleaned_data['latitude'],
                    # geoform.cleaned_data['longitude']
                )
            )
        )
    return JsonResponse({
        'dentists': result
    })

def dentist_page(request):
    body = loads(request.body.decode("utf-8"))
    language = body.get('language') or "uz"
    dentist_slug = body.get("slug")
    print(dentist_slug)
    dentist = Service_translation.objects.filter(service__dentist__slug = dentist_slug).first()
    return JsonResponse({
        'dentist': {
            "name" : Service_translation.dentist.name,
            "" : Service_translation.dentist.name,
            "name" : Service_translation.dentist.name,
            "name" : Service_translation.dentist.name,
            "name" : Service_translation.dentist.name,
        }
    })
