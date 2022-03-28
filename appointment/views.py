from random import randint
from django.conf import settings as global_settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _
from datetime import datetime, date, timedelta
from baseapp.models import *
from dentist.models import User as DentistUser, User_translation as DentistUserTranslation, Service, Service_translation
from illness.models import *
from patient.forms import PatientForm
from patient.models import Key, User as PatientUser
from mydentist.handler import *
from mydentist.var import *
from .forms import *
from .models import *


def appointments(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    is_success = True
    text = None
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    dentist_translation = DentistUserTranslation.objects.filter(
        dentist=dentist,
        language__pk=dentist.language_id
    )[0]
    notifications = get_notifications(request, "dentist")
    queries = get_queries(Query.objects.filter(dentist=dentist))
    if request.method == "POST":
        patientform = AppointmentPatientForm(request.POST)
        appointmentform = AppointmentForm(request.POST)
        if patientform.is_valid() and appointmentform.is_valid():
            name = patientform.cleaned_data['name']
            try:
                phone_number = patientform.cleaned_data['phone_number']
                patient = PatientUser.objects.get(phone_number=phone_number)
                print(patient)
                patient_user = User.objects.get(pk=patient.user_id)
                if not (name.split(" ")[0] == patient_user.last_name and name.split(" ")[1] == patient_user.first_name and phone_number == patient.phone_number and str(patient.birthday) == patientform.cleaned_data['birthday'] and patient.gender_id == int(patientform.cleaned_data['gender']) and patient.address == patientform.cleaned_data['address']):
                    is_success = False
                    text = _("Bemor ma'lumotlari to'g'ri kelmayapti")
            except:
                file_path = global_settings.PROJECT_DIR / "last_id.txt"
                with open(file_path, "r") as file:
                    id = int(file.read()) + 1
                with open(file_path, "w") as file:
                    file.write(str(id))
                id = f"{id:07d}"
                if len(name.split(" ")) > 1:
                    patient_user = User.objects.create_user(
                        f"user{id}",
                        password=f"user{id}",
                        last_name=name.split(" ")[0],
                        first_name=" ".join(name.split(" ")[1:])
                    )
                elif len(name.split(" ")) == 1:
                    patient_user = User.objects.create_user(
                        f"user{id}",
                        password=f"user{id}",
                        first_name=name
                    )
                patient = PatientUser.objects.create(
                    user=patient_user,
                    phone_number=patientform.cleaned_data['phone_number'],
                    address=patientform.cleaned_data['address'],
                    birthday=patientform.cleaned_data['birthday'],
                    image="patients/photos/default.png",
                    language=Language.objects.get(name="ru"),
                    gender=Gender.objects.get(pk=patientform.cleaned_data['gender'])
                )
                key = Key.objects.create(
                    patient=patient,
                    key=randint(100000, 999999)
                )
                dp = Patient.objects.create(
                    dentist=dentist,
                    patient=patient
                )
                success = _("Yangi bemor qo'shildi")
                text = mark_safe(f"{success}{NEW_LINE}{_('Telefon raqam')}: {patient.phone_number}{NEW_LINE}{_('Parol')}: user{id}")
            if is_success:
                service_translation = Service_translation.objects.filter(
                    name=appointmentform.cleaned_data['service'],
                    language__pk=dentist.language_id
                )[0]
                service = Service.objects.get(pk=service_translation.service_id)
                begin = appointmentform.cleaned_data['begin_day']
                begin_day = int(begin.split("-")[0])
                begin_month = MONTHS.index(begin.split("-")[1].split(" ")[0].capitalize()) + 1
                begin_year = int(begin.split(" ")[1])
                begin_hour = int(appointmentform.cleaned_data['begin_time'].split(":")[0])
                begin_minute = int(appointmentform.cleaned_data['begin_time'].split(":")[1])
                begin = datetime(begin_year, begin_month, begin_day, begin_hour, begin_minute, tzinfo=timezone.now().tzinfo)
                duration = int(appointmentform.cleaned_data['duration'])
                duration = timedelta(hours=duration // 60, minutes=duration % 60)
                end = begin + duration
                if compare_appointment(begin, end, Appointment.objects.filter(
                    dentist=dentist,
                    begin__year=begin_year,
                    begin__month=begin_month,
                    begin__day=begin_day
                )):
                    appointment = Appointment.objects.create(
                        dentist=dentist,
                        patient=patient,
                        service=service,
                        begin=begin,
                        end=end,
                        comment=appointmentform.cleaned_data['comment'],
                        status="waiting"
                    )
                    try:
                        query = Query.objects.get(patient=patient)
                        query.delete()
                    except:
                        pass
                    notification = Dentist2patient.objects.create(
                        sender=dentist,
                        recipient=patient,
                        type="appointment",
                        message=f"{service.name}{NEW_LINE}{dentist.id}",
                        datetime=timezone.now() + timedelta(seconds=global_settings.TIME_ZONE_HOUR * 3600),
                        is_read=False
                    )
                else:
                    is_success = False
                    text = _("Ushbu qabulni belgilab bo'lmaydi. Boshqa vaqtni tanlang")
                return redirect("dentx:appointments")
    services = get_services(
        Service.objects.filter(dentist=dentist),
        dentist.language_id
    )
    today = date.today()
    times = []
    day_begin = datetime(
        today.year,
        today.month,
        today.day,
        dentist.worktime_begin.hour,
        dentist.worktime_begin.minute
    )
    day_end = datetime(
        today.year,
        today.month,
        today.day,
        dentist.worktime_end.hour,
        dentist.worktime_end.minute
    )
    while day_begin < day_end:
        times.append(day_begin.strftime('%H:%M'))
        day_begin += timedelta(minutes=15)
    patientform = AppointmentPatientForm()
    appointmentform = AppointmentForm()
    return render(request, "appointment/appointments.html", {
        'patientform': patientform,
        'appointmentform': appointmentform,
        'dentist': dentist,
        'dentist_translation': dentist_translation,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'queries': queries,
        'services': services,
        'times': times,
        'is_success': is_success,
        'text': text
    })


def appointments_update(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        dentist = DentistUser.objects.get(user=user)
        dentist_translation = DentistUserTranslation.objects.filter(
            dentist=dentist,
            language__pk=dentist.language_id
        )[0]
        patientform = PatientForm(request.POST)
        appointmentform = AppointmentForm(request.POST)
        if patientform.is_valid() and appointmentform.is_valid():
            print(request.POST.get('appointment_id'))
            name = patientform.cleaned_data['name'].split(" ")
            phone_number = patientform.cleaned_data['phone_number']
            try:
                patient = PatientUser.objects.get(phone_number=phone_number)
                patient_user = User.objects.get(pk=patient.user_id)
                if len(name) > 1:
                    user_check = name[0] == patient_user.last_name and " ".join(name[1:]) == patient_user.first_name
                elif len(name) == 1:
                    user_check = name[0] == patient_user.first_name
                if user_check and phone_number == patient.phone_number and str(patient.birthday) == patientform.cleaned_data['birthday'] and patient.gender_id == int(patientform.cleaned_data['gender']) and patient.address == patientform.cleaned_data['address']:
                    print(request.POST)
                    service_translation = Service_translation.objects.filter(
                        name=appointmentform.cleaned_data['service'],
                        language__pk=dentist.language_id
                    )[0]
                    service = Service.objects.get(pk=service_translation.service_id)
                    begin = appointmentform.cleaned_data['begin_day']
                    begin_day = int(begin.split("-")[0])
                    begin_month = MONTHS.index(begin.split("-")[1].split(" ")[0].capitalize()) + 1
                    begin_year = int(begin.split(" ")[1])
                    begin_hour = int(appointmentform.cleaned_data['begin_time'].split(":")[0])
                    begin_minute = int(appointmentform.cleaned_data['begin_time'].split(":")[1])
                    begin = datetime(begin_year, begin_month, begin_day, begin_hour, begin_minute, tzinfo=timezone.now().tzinfo)
                    duration = int(appointmentform.cleaned_data['duration'])
                    duration = timedelta(hours=duration // 60, minutes=duration % 60)
                    end = begin + duration
                    try:
                        last_begin = request.session['date']
                        last_begin_day = int(last_begin.split("-")[0])
                        last_begin_month = MONTHS.index(last_begin.split("-")[1].split(" ")[0].capitalize()) + 1
                        last_begin_year = int(last_begin.split(" ")[1])
                        last_begin_hour = int(request.session['time'].split(":")[0])
                        last_begin_minute = int(request.session['time'].split(":")[1])
                        last_begin = datetime(last_begin_year, last_begin_month, last_begin_day, last_begin_hour, last_begin_minute, tzinfo=timezone.now().tzinfo)
                        appointment = Appointment.objects.get(
                            dentist=dentist,
                            begin=last_begin,
                        )
                        appointment.patient_id = patient.id
                        appointment.service_id = service.id
                        appointment.begin = begin
                        appointment.end = end
                        appointment.comment = appointmentform.cleaned_data["comment"]
                        appointment.save()
                    except Exception as E:
                        print(E)
                else:
                    pass
            except:
                pass
        return redirect("dentx:appointments")


def status_update(request):
    if request.method == "POST":
        appointment = Appointment.objects.get(pk=int(request.POST['id']))
        if request.POST['status'] == _("Kutilmoqda"):
            appointment.status = "done"
        elif request.POST['status'] == _("Kelgan"):
            appointment.status = "missed"
        elif request.POST['status'] == _("Kelmagan"):
            appointment.status = "waiting"
        appointment.save()
        return HttpResponse(request.POST['id'])


def appointments_delete(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    try:
        date = request.POST['delete_date'].split("<br>")[0]
        request.session['date'] = date
        day = date.split("-")[0]
        month = MONTHS.index(date.split("-")[1].split(" ")[0].capitalize()) + 1
        year = date.split(" ")[1]
        time = request.POST['delete_time']
        request.session['time'] = time
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        appointment = Appointment.objects.filter(
            dentist__user__username=request.user.username,
            begin__year=year,
            begin__month=month,
            begin__day=day,
            begin__hour=hour,
            begin__minute=minute
        ).first()
        if appointment:
            appointment.delete()
    except:
        pass
    return redirect("dentx:appointments")


def table(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        if request.POST['direction'] == "left":
            day = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            ) - timedelta(weeks=1)
        elif request.POST['direction'] == "right":
            temp = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            )
            day = temp + timedelta(days=temp.weekday(), weeks=1)
    else:
        temp = date.today()
        day = temp - timedelta(days=temp.weekday())
    days = [day]
    html = f"<table class=\"time-table table-bordered text-center\"><thead><tr class=\"text-center\"><th>Time</th><th>{day.day}-{MONTHS[day.month - 1].lower()} {day.year}<br>{DAYS[day.weekday()]}</th>"
    for i in range(6):
        temp = days[len(days) - 1] + timedelta(days=1)
        days.append(temp)
        html += f"<th>{temp.day}-{MONTHS[temp.month - 1].lower()} {temp.year}<br>{DAYS[temp.weekday()]}</th>"
    html += "</tr></thead><tbody>"
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    day_begin = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_begin.hour,
        dentist.worktime_begin.minute
    )
    day_end = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_end.hour,
        dentist.worktime_end.minute
    )
    while day_begin <= day_end:
        html += f"<tr><th>{day_begin.strftime('%H:%M')}</th>"
        for day in days:
            time = datetime(
                day.year,
                day.month,
                day.day,
                day_begin.hour,
                day_begin.minute,
                tzinfo=timezone.now().tzinfo
            )
            html += compare_time(time, Appointment.objects.filter(
                dentist=dentist,
                begin__year=time.year,
                begin__month=time.month,
                begin__day=time.day
            ))
        day_begin += timedelta(minutes=15)
        html += "</tr>"
    html += "</tbody></table><script type='text/javascript'>$('.overflow').css({'overflow-x': 'scroll','overflow-y': 'scroll','height': '45vh'})</script>"
    return HttpResponse(html)


def test_table(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        if request.POST['direction'] == "left":
            day = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            ) - timedelta(weeks=1)
        elif request.POST['direction'] == "right":
            temp = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            )
            day = temp + timedelta(days=temp.weekday(), weeks=1)
        else:
            temp = date.today()
            day = temp - timedelta(days=temp.weekday())
    else:
        temp = date.today()
        day = temp - timedelta(days=temp.weekday())
    days = [day]
    table = [
        [
            {
                'name': "Vaqt"
            },
            {
                'day': day.strftime("%d.%m.%Y"),
                'name': f"{DAYS[day.weekday()]}<br>{day.day}-{MONTHS[day.month - 1].lower()}",
                'old_name': f"{day.day}-{MONTHS[day.month - 1].lower()} {day.year}<br>{DAYS[day.weekday()]}"
            }
        ]
    ]
    dentist = DentistUser.objects.get(user=request.user)
    for i in range(dentist.work_days - 1):
        temp = days[-1] + timedelta(days=1)
        days.append(temp)
        table[0].append({
            'day': temp.strftime("%d.%m.%Y"),
            'name': f"{DAYS[temp.weekday()]}<br>{temp.day}-{MONTHS[temp.month - 1].lower()}",
            'old_name': f"{temp.day}-{MONTHS[temp.month - 1].lower()} {temp.year}<br>{DAYS[temp.weekday()]}"
        })
    day_begin = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_begin.hour,
        dentist.worktime_begin.minute
    )
    day_end = datetime(
        days[0].year,
        days[0].month,
        days[0].day,
        dentist.worktime_end.hour,
        dentist.worktime_end.minute
    )
    while day_begin <= day_end:
        table.append([])
        table[-1].append({
            'class': "",
            'name': day_begin.strftime('%H:%M')
        })
        for day in days:
            time = datetime(
                day.year,
                day.month,
                day.day,
                day_begin.hour,
                day_begin.minute,
                tzinfo=timezone.now().tzinfo
            )
            table[-1].append(test_compare_time(
                time,
                Appointment.objects.filter(
                    dentist=dentist,
                    begin__year=time.year,
                    begin__month=time.month,
                    begin__day=time.day
                )
            ))
        day_begin += timedelta(minutes=15)
    return JsonResponse(table, safe=False)


def patients(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    patients = []
    temp = [ PatientUser.objects.get(pk=patient.patient_id) for patient in Patient.objects.filter(dentist__user=request.user) ]
    for patient in temp:
        patients.append({
            'image': str(patient.image),
            'name': str(patient),
            'phone_number': patient.phone_number,
            'birthday': str(patient.birthday),
            'gender': patient.gender_id,
            'address': patient.address
        })
    return JsonResponse(patients, safe=False)


def appointment(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    try:
        date = request.POST['date'].split("<br>")[0]
        request.session['date'] = date
        day = date.split("-")[0]
        month = MONTHS.index(date.split("-")[1].split(" ")[0].capitalize()) + 1
        year = date.split(" ")[1]
        time = request.POST['time']
        request.session['time'] = time
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        appointment = Appointment.objects.get(
            dentist__user__username=request.user.username,
            begin__year=year,
            begin__month=month,
            begin__day=day,
            begin__hour=hour,
            begin__minute=minute,
        )
        patient = PatientUser.objects.get(pk=appointment.patient_id)
        service = Service_translation.objects.get(
            service__pk=appointment.service_id,
            language__name=get_language()
        )
        return JsonResponse({
            'id': appointment.id,
            'name': str(patient),
            'phone_number': patient.phone_number,
            'birthday': str(patient.birthday),
            'gender': patient.gender_id,
            'address': patient.address,
            'service': service.name,
            'duration': (appointment.end - appointment.begin).seconds // 60,
            'comment': appointment.comment,
            'date': request.POST['date'],
            'time': time
        }, safe=False)
    except:
        return JsonResponse({}, safe=False)
