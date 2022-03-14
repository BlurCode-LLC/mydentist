from django.db.models import Count
from django.http import JsonResponse
from django.utils import translation
from json import loads

from dentist.models import Service_translation, User as DentistUser
from mydentist.var import REGIONS


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
    hour_24 = body.get("hour_24")
    no_que = body.get("no_que")

    dentist_object = DentistUser.objects.filter(
        clinic__region = region,

    )

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
