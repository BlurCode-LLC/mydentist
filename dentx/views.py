from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from appointment.models import *
from dentist.models import Animation, Animation_translation, User as DentistUser, Reminder
from mydentist.handler import *


def board(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    notifications = get_notifications(request, "dentist")
    appointments_waiting = get_appointments(Appointment.objects.filter(
        dentist=dentist,
        status="waiting"
    ).order_by("begin"))
    appointments_done = get_appointments(Appointment.objects.filter(
        dentist=dentist,
        status="done"
    ))
    appointments_missed = get_appointments(Appointment.objects.filter(
        dentist=dentist,
        status="missed"
    ))
    return render(request, "dentx/board.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'appointments_waiting': appointments_waiting,
        'appointments_done': appointments_done,
        'appointments_missed': appointments_missed,
    })


def reminders(request):
    dentist = DentistUser.objects.get(user__username=request.user.username)
    if request.method == "POST":
        if request.POST['type'] == "add":
            reminder = Reminder.objects.create(
                dentist=dentist,
                name=request.POST['name'],
                category=request.POST['category'],
                is_done=False
            )
        elif request.POST['type'] == "edit":
            if 'is_done' in request.POST:
                reminder = Reminder.objects.get(pk=int(request.POST['id']))
                if request.POST['is_done'] == "true":
                    reminder.is_done = True
                elif request.POST['is_done'] == "false":
                    reminder.is_done = False
                reminder.save()
            else:
                reminder = Reminder.objects.get(pk=int(request.POST['id']))
                reminder.name = request.POST['name']
                reminder.save()
        elif request.POST['type'] == "delete":
            reminder = Reminder.objects.get(pk=int(request.POST['id']))
            reminder.delete()
        return redirect("dentx:reminders")
    reminders_do = get_reminders(Reminder.objects.filter(
        dentist=dentist,
        category="do"
    ))
    reminders_buy = get_reminders(Reminder.objects.filter(
        dentist=dentist,
        category="buy"
    ))
    return JsonResponse({
        "do": reminders_do,
        "buy": reminders_buy
    }, safe=False)


def animations(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    notifications = get_notifications(request, "dentist")
    animations_obj = Animation.objects.all()
    animations = []
    for animation_obj in animations_obj:
        trans = animation_obj.animation_translation.filter(language__pk=dentist.language_id).first()
        animations.append({
            'animation': animation_obj,
            'translation': trans
        })
    return render(request, "dentx/animations.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'animations': animations
    })
