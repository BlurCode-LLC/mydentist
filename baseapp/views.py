from datetime import date
from django.conf import settings as global_settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _, get_language
from json import dumps
from telebot import TeleBot
from dentist.models import Service_category, Service_category_translation, User as DentistUser, Service_translation
from patient.models import User as PatientUser
from mydentist.handler import *
from mydentist.var import REGIONS
from .forms import *
from .models import *


def error_404(request, exception):
    return render(request, "http/404.html", {
        'exception': exception
    })


def error_403(request, exception):
    return render(request, "http/403.html")


def index(request):
    if request.method == "POST":
        temp = {}
        from html import unescape
        for key, value in request.POST.items():
            temp[key] = unescape(value) if isinstance(value, str) else value
        request.session['post'] = temp
        return redirect("baseapp:results")
    else:
        try:
            del request.session['post']
        except:
            pass
        searchform = SearchForm()
        geoform = GeoForm()
        authenticated = is_authenticated(request, "patient") or is_authenticated(request, "dentist")
        if authenticated:
            try:
                user = PatientUser.objects.get(user__username=request.user.username)
                authenticated = "patient"
                check_language(request, "patient")
            except:
                try:
                    user = DentistUser.objects.get(user__username=request.user.username)
                    authenticated = "dentist"
                except:
                    pass
        language = Language.objects.get(name=get_language())
        services = [{
            'value': item.service_category_id,
            'name': item.name
        } for item in Service_category_translation.objects.filter(language=language)]
        return render(request, "baseapp/index.html", {
            'searchform': searchform,
            'regions': REGIONS,
            'region': REGIONS[0],
            'services': services,
            'service': services[0],
            'geoform': geoform,
            'authenticated': authenticated
        })


def results(request):
    authenticated = is_authenticated(request, "patient") or is_authenticated(request, "dentist")
    if authenticated:
        try:
            user = PatientUser.objects.get(
                user__username=request.user.username)
            authenticated = "patient"
            check_language(request, "patient")
        except:
            try:
                user = DentistUser.objects.get(
                    user__username=request.user.username)
                authenticated = "dentist"
            except:
                pass
    return render(request, "baseapp/results.html", {
        'authenticated': authenticated
    })


def get_dentists(request):
    if 'post' in request.session:
        current_language = get_language()
        searchform = SearchForm(request.session['post'])
        geoform = GeoForm(request.session['post'])
        if searchform.is_valid() and geoform.is_valid():
            print(request.session['post'])
            def searcher():
                if request.POST['female'] == "true" and request.POST['queue'] == "true" and request.POST['time'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        language__name=current_language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True,
                        service__dentist__is_queued=True
                    )
                elif request.POST['female'] == "true" and request.POST['queue'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        language__name=current_language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_queued=True
                    )
                elif request.POST['female'] == "true" and request.POST['time'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        language__name=current_language,
                        service__dentist__gender__pk=2,
                        service__dentist__is_fullday=True
                    )
                elif request.POST['queue'] == "true" and request.POST['time'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        language__name=current_language,
                        service__dentist__is_fullday=True,
                        service__dentist__is_queued=True
                    )
                elif request.POST['female'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__gender__pk=2,
                        language__name=current_language
                    )
                elif request.POST['queue'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        language__name=current_language,
                        service__dentist__is_queued=True
                    )
                elif request.POST['time'] == "true":
                    return Service_translation.objects.filter(
                        service__service_category__pk=searchform.cleaned_data['service'],
                        service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                        service__dentist__is_fullday=True,
                        language__name=current_language
                    )
                return Service_translation.objects.filter(
                    service__service_category__pk=searchform.cleaned_data['service'],
                    service__dentist__clinic__region__pk=searchform.cleaned_data['region'],
                    language__name=current_language
                )
            if geoform.cleaned_data['latitude'] is not None and geoform.cleaned_data['longitude'] is not None:
                location = (geoform.cleaned_data['latitude'], geoform.cleaned_data['longitude'])
                services_obj = searcher()
                if request.POST.get('sort_by') == "near":
                    results = get_results(sort_by_distance(list(services_obj), location), location)
                else:
                    results = get_results(list(services_obj.order_by('service__price')), location)
                response = HttpResponse(dumps(results))
            else:
                response = HttpResponse(dumps([]))
            return response
        else:
            response = HttpResponse()
            response.status_code = 404
            return response
    else:
        response = HttpResponse()
        response.status_code = 404
        return response


def send_message(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        print(global_settings)
        # bot = TeleBot()
        bot = TeleBot("1965697713:AAFeZXqE3Q-xtqU7-v0fr81X9B4HjQ726y4")
        if name and phone:
            bot.send_message(657368864, f"<b>{name}</b> ismli va {phone} raqamli foydalanuvchi siz bilan bog'lanmoqchi", parse_mode="HTML")
        return redirect(request.META.get("HTTP_REFERER", "/"))
