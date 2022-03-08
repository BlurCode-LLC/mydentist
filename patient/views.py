from datetime import datetime, date
from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from appointment.models import Query, Appointment
from baseapp.models import Language, Gender
from dentist.models import User as DentistUser, User_translation, Clinic, Clinic_translation, Service, Service_translation, Cabinet_Image
from illness.models import *
from illness.forms import *
from login.forms import PasswordUpdateForm
from mydentist.handler import *
from mydentist.var import *
from .forms import *
from .models import User as PatientUser, Illness, Other_Illness, Process_photo


def profile(request):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "patient")
    user = User.objects.get(username=request.user.username)
    user_extra = PatientUser.objects.get(user=user)
    notifications = get_notifications(request, "patient")
    try:
        try:
            appointments = Appointment.objects.filter(patient=user_extra).order_by("begin")
            for appointment_obj in appointments:
                if appointment_obj.upcoming():
                    appointment = appointment_obj
                    break
            query = None
            dentist = DentistUser.objects.get(pk=appointment.dentist_id)
            dentist_extra = User_translation.objects.get(dentist=dentist, language__pk=user_extra.language_id)
            clinic = Clinic.objects.get(pk=dentist.clinic_id)
            clinic_extra = Clinic_translation.objects.get(clinic=clinic, language__pk=user_extra.language_id)
            cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist.id)
            try:
                services_obj = Service_translation.objects.filter(language__pk=user_extra.language_id, service__dentist=dentist)
                services = []
                for service_extra in services_obj:
                    services.append({
                        'service': Service.objects.get(pk=service_extra.service_id),
                        'service_extra': service_extra
                    })
            except:
                services = []
        except:
            appointment = None
            query = Query.objects.get(patient=user_extra)
            dentist = DentistUser.objects.get(pk=query.dentist_id)
            dentist_extra = User_translation.objects.get(dentist=dentist, language__pk=user_extra.language_id)
            clinic = Clinic.objects.get(pk=dentist.clinic_id)
            clinic_extra = Clinic_translation.objects.get(clinic=clinic, language__pk=user_extra.language_id)
            cabinet_images = Cabinet_Image.objects.filter(dentist__pk=dentist.id)
            try:
                services_obj = Service_translation.objects.filter(language__pk=user_extra.language_id, service__dentist=dentist)
                services = []
                for service_extra in services_obj:
                    services.append({
                        'service': Service.objects.get(pk=service_extra.service_id),
                        'service_extra': service_extra
                    })
            except:
                services = []
    except:
        appointment = None
        query = None
        dentist = None
        dentist_extra = None
        clinic = None
        clinic_extra = None
        cabinet_images = []
        services = []
    authenticated = is_authenticated(request, "patient")
    if authenticated:
        try:
            user = PatientUser.objects.get(
                user__username=request.user.username)
            authenticated = "patient"
            check_language(request, "patient")
        except:
            try:
                user = DentistUser.objects.get(user__username=request.user.username)
                authenticated = "dentist"
            except:
                pass
    if len(cabinet_images) > 1:
        counter = range(len(cabinet_images))
        cabinet_image = cabinet_images[0]
        cabinet_images = cabinet_images[1:]
    elif len(cabinet_images) == 1:
        counter = range(1)
        cabinet_image = cabinet_images[0]
        cabinet_images = None
    else:
        counter = 0
        cabinet_image = None
        cabinet_images = None
    return render(request, "patient/profile.html", {
        'user_extra': user_extra,
        'appointment': appointment,
        'dentist': dentist,
        'dentist_extra': dentist_extra,
        'clinic': clinic,
        'clinic_extra': clinic_extra,
        'services': services,
        'cabinet_image': cabinet_image,
        'cabinet_images': cabinet_images,
        'counter': counter,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'authenticated': authenticated,
    })


def settings(request, active_tab="profile"):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "patient")
    if 'success_message' in request.session:
        if request.session['success_message'] == "Updated successfully":
            success_message = "Updated successfully"
        elif request.session['success_message'] == "Passwords do not match":
            success_message = "Passwords do not match"
        del request.session['success_message']
    else:
        success_message = None
    user = User.objects.get(username=request.user.username)
    user_extra = PatientUser.objects.get(user=user)
    userform = UserForm({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user_extra.gender_id,
        'birth_year': user_extra.birthday.year,
        'birth_month': MONTHS[user_extra.birthday.month - 1],
        'birth_day': user_extra.birthday.day,
        'phone_number': user_extra.phone_number,
        'email': user.email,
        'address': user_extra.address,
    })
    languageform = LanguageForm({
        'language': user_extra.language_id
    })
    if 'incorrect_password' in request.session:
        passwordupdateform = PasswordUpdateForm(request.session['incorrect_password'])
        del request.session['incorrect_password']
    else:
        passwordupdateform = PasswordUpdateForm()
    illness = Illness.objects.get(patient=user_extra)
    illnessform = IllnessForm({
        'diabet': Diabet.objects.get(pk=illness.diabet_id).value if illness.diabet_id is not None else None,
        'anesthesia': Anesthesia.objects.get(pk=illness.anesthesia_id).value if illness.anesthesia_id is not None else None,
        'hepatitis': Hepatitis.objects.get(pk=illness.hepatitis_id).value if illness.hepatitis_id is not None else None,
        'aids': AIDS.objects.get(pk=illness.aids_id).value if illness.aids_id is not None else None,
        'pressure': Pressure.objects.get(pk=illness.pressure_id).value if illness.pressure_id is not None else None,
        'allergy': Allergy.objects.get(pk=illness.allergy_id).value if illness.allergy_id is not None else None,
        'allergy_detail': Allergy.objects.get(pk=illness.allergy_id).desc if illness.allergy_id is not None else None,
        'asthma': Asthma.objects.get(pk=illness.asthma_id).value if illness.asthma_id is not None else None,
        'dizziness': Dizziness.objects.get(pk=illness.dizziness_id).value if illness.dizziness_id is not None else None,
    })
    otherillness = Other_Illness.objects.get(patient=user_extra)
    otherillnessform = OtherIllnessForm({
        'epilepsy': Epilepsy.objects.get(pk=otherillness.epilepsy_id).value if otherillness.epilepsy_id is not None else None,
        'blood_disease': Blood_disease.objects.get(pk=otherillness.blood_disease_id).value if otherillness.blood_disease_id is not None else None,
        'medications': Medications.objects.get(pk=otherillness.medications_id).value if otherillness.medications_id is not None else None,
        'medications_detail': Medications.objects.get(pk=otherillness.medications_id).desc if otherillness.medications_id is not None else None,
        'stroke': Stroke.objects.get(pk=otherillness.stroke_id).value if otherillness.stroke_id is not None else None,
        'heart_attack': Heart_attack.objects.get(pk=otherillness.heart_attack_id).value if otherillness.heart_attack_id is not None else None,
        'oncologic': Oncologic.objects.get(pk=otherillness.oncologic_id).value if otherillness.oncologic_id is not None else None,
        'tuberculosis': Tuberculosis.objects.get(pk=otherillness.tuberculosis_id).value if otherillness.tuberculosis_id is not None else None,
        'alcohol': Alcohol.objects.get(pk=otherillness.alcohol_id).value if otherillness.alcohol_id is not None else None,
        'pregnancy': Pregnancy.objects.get(pk=otherillness.pregnancy_id).value if otherillness.pregnancy_id is not None else None,
        'pregnancy_detail': Pregnancy.objects.get(pk=otherillness.pregnancy_id).desc if otherillness.pregnancy_id is not None else None,
    })
    authenticated = is_authenticated(request, "patient")
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
    return render(request, "patient/settings.html", {
        'userform': userform,
        'languageform': languageform,
        'passwordupdateform': passwordupdateform,
        'illnessform': illnessform,
        'otherillnessform': otherillnessform,
        'active_tab': active_tab,
        'success_message': success_message,
        'authenticated': authenticated,
        'user': user,
        'user_extra': user_extra
    })


def update(request, form):
    if not is_authenticated(request, "patient"):
        if not is_authenticated(request, "dentist"):
            return redirect(f"{global_settings.LOGIN_URL}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "patient")
    if request.method == "POST":
        if form == "profile":
            userform = UserForm(request.POST)
            languageform = LanguageForm(request.POST)
            if userform.is_valid() and languageform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                user.first_name = userform.cleaned_data['first_name']
                user.last_name = userform.cleaned_data['last_name']
                user_extra.gender_id = userform.cleaned_data['gender']
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                user_extra.birthday = datetime(year, month, day)
                user_extra.phone_number = userform.cleaned_data['phone_number']
                user.email = userform.cleaned_data['email']
                user_extra.address = userform.cleaned_data['address']
                user_extra.language_id = languageform.cleaned_data['language']
                language = Language.objects.get(pk=user_extra.language_id).name
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                user.save()
                user_extra.save()
                passwordupdateform = PasswordUpdateForm(request.POST)
                illnessform = IllnessForm(request.POST)
                otherillnessform = OtherIllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="profile")
        elif form == "password":
            passwordupdateform = PasswordUpdateForm(request.POST)
            if passwordupdateform.is_valid():
                user = User.objects.get(username=request.user.username)
                if user.check_password(passwordupdateform.cleaned_data['old_password']) and passwordupdateform.cleaned_data['password'] == passwordupdateform.cleaned_data['password_confirm']:
                    username = user.username
                    user.set_password(passwordupdateform.cleaned_data['password'])
                    user.save()
                    user = authenticate(
                        request,
                        username=username,
                        password=passwordupdateform.cleaned_data['password']
                    )
                    login(request, user)
                    patient = PatientUser.objects.get(user=user)
                    language = Language.objects.get(pk=patient.language_id).name
                    translation.activate(language)
                    request.session[translation.LANGUAGE_SESSION_KEY] = language
                    request.session[user.get_username()] = user.get_username()
                    userform = UserForm(request.POST)
                    illnessform = IllnessForm(request.POST)
                    otherillnessform = OtherIllnessForm(request.POST)
                    request.session['success_message'] = "Updated successfully"
                    return redirect("patient:settings", active_tab="password")
                else:
                    request.session['incorrect_password'] = {
                        'old_password': passwordupdateform.cleaned_data['old_password'],
                        'password': passwordupdateform.cleaned_data['password'],
                        'password_confirm': passwordupdateform.cleaned_data['password_confirm']
                    }
                    userform = UserForm(request.POST)
                    languageform = LanguageForm(request.POST)
                    illnessform = IllnessForm(request.POST)
                    otherillnessform = OtherIllnessForm(request.POST)
                    request.session['success_message'] = "Passwords do not match"
                    return redirect("patient:settings", active_tab="password")
        elif form == "illness":
            illnessform = IllnessForm(request.POST)
            if illnessform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                illness = Illness.objects.get(user=user_extra)
                if illnessform.cleaned_data['allergy'] == 2:
                    try:
                        allergy = Allergy.objects.get(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                    except:
                        allergy = Allergy.objects.create(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                else:
                    allergy = Allergy.objects.get(
                        value=illnessform.cleaned_data['allergy'],
                    )
                illness.diabet_id = Diabet.objects.get(value=illnessform.cleaned_data['diabet']).id
                illness.anesthesia_id = Anesthesia.objects.get(value=illnessform.cleaned_data['anesthesia']).id
                illness.hepatitis_id = Hepatitis.objects.get(value=illnessform.cleaned_data['hepatitis']).id
                illness.aids_id = AIDS.objects.get(value=illnessform.cleaned_data['aids']).id
                illness.pressure_id = Pressure.objects.get(value=illnessform.cleaned_data['pressure']).id
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=illnessform.cleaned_data['asthma']).id
                illness.dizziness_id = Dizziness.objects.get(value=illnessform.cleaned_data['dizziness']).id
                illness.save()
                userform = UserForm(request.POST)
                languageform = LanguageForm(request.POST)
                passwordupdateform = PasswordUpdateForm(request.POST)
                otherillnessform = OtherIllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="illness")
        elif form == "other-illness":
            otherillnessform = OtherIllnessForm(request.POST)
            if otherillnessform.is_valid():
                user = User.objects.get(username=request.user.username)
                user_extra = PatientUser.objects.get(user=user)
                otherillness = Other_Illness.objects.get(user=user_extra)
                if otherillnessform.cleaned_data['medications'] == 2:
                    try:
                        medications = Medications.objects.get(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                    except:
                        medications = Medications.objects.create(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                else:
                    medications = Medications.objects.get(
                        value=otherillnessform.cleaned_data['medications'],
                    )
                if otherillnessform.cleaned_data['pregnancy'] == 2:
                    try:
                        pregnancy = Pregnancy.objects.get(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                    except:
                        pregnancy = Pregnancy.objects.create(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                else:
                    pregnancy = Pregnancy.objects.get(
                        value=otherillnessform.cleaned_data['pregnancy'],
                    )
                otherillness.epilepsy_id = Epilepsy.objects.get(value=otherillnessform.cleaned_data['epilepsy']).id
                otherillness.blood_disease_id = Blood_disease.objects.get(value=otherillnessform.cleaned_data['blood_disease']).id
                otherillness.medications_id = medications.id
                otherillness.stroke_id = Stroke.objects.get(value=otherillnessform.cleaned_data['stroke']).id
                otherillness.heart_attack_id = Heart_attack.objects.get(value=otherillnessform.cleaned_data['heart_attack']).id
                otherillness.oncologic_id = Oncologic.objects.get(value=otherillnessform.cleaned_data['oncologic']).id
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=otherillnessform.cleaned_data['tuberculosis']).id
                otherillness.alcohol_id = Alcohol.objects.get(value=otherillnessform.cleaned_data['alcohol']).id
                otherillness.pregnancy_id = pregnancy.id
                otherillness.save()
                userform = UserForm(request.POST)
                languageform = LanguageForm(request.POST)
                passwordupdateform = PasswordUpdateForm(request.POST)
                illnessform = IllnessForm(request.POST)
                request.session['success_message'] = "Updated successfully"
                return redirect("patient:settings", active_tab="other-illness")
        return redirect("patient:settings", active_tab="profile")


def update_photo(request):
    if request.method == "POST":
        photo = request.FILES.get("file")
        patient = PatientUser.objects.get(user=request.user)
        patient.image = photo
        patient.save()
        return JsonResponse({
            'photo': patient.image.url
        }, safe=False)


def patients(request):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    if 'text' in request.session:
        text = request.session['text']
        del request.session['text']
    else:
        text = None
    user = User.objects.get(username=request.user.username)
    dentist = DentistUser.objects.get(user=user)
    notifications = get_notifications(request, "dentist")
    queries = get_queries(Query.objects.filter(dentist=dentist))
    if request.method == "POST":
        patientform = PatientForm(request.POST)
        languageform = LanguageForm(request.POST)
        if patientform.is_valid() and languageform.is_valid():
            try:
                new_patient = PatientUser.objects.get(phone_number=patientform.cleaned_data['phone_number'])
            except:
                file_path = global_settings.PROJECT_DIR / "last_id.txt"
                with open(file_path, "r") as file:
                    id = int(file.read()) + 1
                with open(file_path, "w") as file:
                    file.write(str(id))
                id = f"{id:07d}"
                name = patientform.cleaned_data['name']
                if len(name.split(" ")) > 1:
                    new_user = User.objects.create_user(
                        f"user{id}",
                        password=f"user{id}",
                        last_name=name.split(" ")[0],
                        first_name=" ".join(name.split(" ")[1:])
                    )
                else:
                    new_user = User.objects.create_user(
                        f"user{id}",
                        password=f"user{id}",
                        first_name=name
                    )
                new_patient = PatientUser.objects.create(
                    user=new_user,
                    phone_number=patientform.cleaned_data['phone_number'],
                    address=patientform.cleaned_data['address'],
                    birthday=patientform.cleaned_data['birthday'],
                    image="patients/photos/default.png",
                    language=Language.objects.get(pk=languageform.cleaned_data['language']),
                    gender=Gender.objects.get(pk=patientform.cleaned_data['gender'])
                )
                success = _("Yangi bemor qo'shildi")
                request.session['text'] = mark_safe(f"{success}{NEW_LINE}{_('Telefon raqam')}: {new_patient.phone_number}{NEW_LINE}{_('Parol')}: user{id}")
                return redirect("dentx:patients")
    results = get_patients(request)
    patientform = PatientForm()
    languageform = LanguageForm()
    return render(request, "patient/patients.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'queries': queries,
        'results': results,
        'patientform': patientform,
        'languageform': languageform,
        'text': text
    })


def search(request):
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
    queries = get_queries(Query.objects.filter(dentist=dentist))
    search = request.GET['search']
    patients = [User.objects.get(pk=patient.user_id) for patient in PatientUser.objects.all()]
    results = []
    for patient in patients:
        if f"{patient.first_name} {patient.last_name}".lower().find(search.lower()) != -1 or f"{patient.last_name} {patient.first_name}".lower().find(search.lower()) != -1:
            patient_extra = PatientUser.objects.get(user=patient)
            appointments = Appointment.objects.filter(
                patient=patient_extra
            )
            done = mark_safe(f", {NEW_LINE}".join([Service_translation.objects.get(
                service__pk=appointment.service_id,
                language__name=get_language()
            ).name for appointment in appointments.filter(status="done").order_by("begin")]))
            total_sum = sum([Service.objects.get(
                pk=appointment.service_id
            ).price for appointment in appointments.filter(status="done")])
            coming = "-"
            for appointment in appointments.filter(status="waiting").order_by("begin"):
                if appointment.upcoming():
                    coming = Service_translation.objects.get(
                        service__pk=appointment.service_id,
                        language__name=get_language()
                    ).name
                    break
            last = appointments.filter(status="done").order_by("-begin").first()
            last_visit = last.begin if last else "-"
            results.append({
                'patient': str(patient_extra),
                'id': patient_extra.id,
                'image': patient_extra.image.url,
                'birthday': patient_extra.birthday.year,
                'phone_number': patient_extra.phone_number,
                'address': patient_extra.address,
                'gender': GENDERS[patient_extra.gender_id - 1],
                'done': done if done != "" else "-",
                'total_sum': total_sum,
                'coming': coming,
                'last_visit': last_visit
            })
    return render(request, "patient/search.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'queries': queries,
        'search': search,
        'results': results
    })


def patient(request, id, active_tab="profile"):
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
    queries = get_queries(Query.objects.filter(dentist=dentist))
    patient_extra = PatientUser.objects.get(pk=id)
    patient = User.objects.get(pk=patient_extra.user_id)
    year = (date.today() - patient_extra.birthday).days // 365
    gender = GENDERS[patient_extra.gender_id - 1]
    userform = UserForm({
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'gender': patient_extra.gender_id,
        'birth_year': patient_extra.birthday.year,
        'birth_month': MONTHS[patient_extra.birthday.month - 1],
        'birth_day': patient_extra.birthday.day,
        'phone_number': patient_extra.phone_number,
        'email': patient.email,
        'address': patient_extra.address,
    })
    patient_illness = Illness.objects.get(patient=patient_extra)
    illnessform = IllnessForm({
        'diabet': Diabet.objects.get(pk=patient_illness.diabet_id).value if patient_illness.diabet_id is not None else None,
        'anesthesia': Anesthesia.objects.get(pk=patient_illness.anesthesia_id).value if patient_illness.anesthesia_id is not None else None,
        'hepatitis': Hepatitis.objects.get(pk=patient_illness.hepatitis_id).value if patient_illness.hepatitis_id is not None else None,
        'aids': AIDS.objects.get(pk=patient_illness.aids_id).value if patient_illness.aids_id is not None else None,
        'pressure': Pressure.objects.get(pk=patient_illness.pressure_id).value if patient_illness.pressure_id is not None else None,
        'allergy': Allergy.objects.get(pk=patient_illness.allergy_id).value if patient_illness.allergy_id is not None else None,
        'allergy_detail': Allergy.objects.get(pk=patient_illness.allergy_id).desc if patient_illness.allergy_id is not None else None,
        'asthma': Asthma.objects.get(pk=patient_illness.asthma_id).value if patient_illness.asthma_id is not None else None,
        'dizziness': Dizziness.objects.get(pk=patient_illness.dizziness_id).value if patient_illness.dizziness_id is not None else None,
    })
    patient_other_illness = Other_Illness.objects.get(patient=patient_extra)
    otherillnessform = OtherIllnessForm({
        'epilepsy': Epilepsy.objects.get(pk=patient_other_illness.epilepsy_id).value if patient_other_illness.epilepsy_id is not None else None,
        'blood_disease': Blood_disease.objects.get(pk=patient_other_illness.blood_disease_id).value if patient_other_illness.blood_disease_id is not None else None,
        'medications': Medications.objects.get(pk=patient_other_illness.medications_id).value if patient_other_illness.medications_id is not None else None,
        'medications_detail': Medications.objects.get(pk=patient_other_illness.medications_id).desc if patient_other_illness.medications_id is not None else None,
        'stroke': Stroke.objects.get(pk=patient_other_illness.stroke_id).value if patient_other_illness.stroke_id is not None else None,
        'heart_attack': Heart_attack.objects.get(pk=patient_other_illness.heart_attack_id).value if patient_other_illness.heart_attack_id is not None else None,
        'oncologic': Oncologic.objects.get(pk=patient_other_illness.oncologic_id).value if patient_other_illness.oncologic_id is not None else None,
        'tuberculosis': Tuberculosis.objects.get(pk=patient_other_illness.tuberculosis_id).value if patient_other_illness.tuberculosis_id is not None else None,
        'alcohol': Alcohol.objects.get(pk=patient_other_illness.alcohol_id).value if patient_other_illness.alcohol_id is not None else None,
        'pregnancy': Pregnancy.objects.get(pk=patient_other_illness.pregnancy_id).value if patient_other_illness.pregnancy_id is not None else None,
        'pregnancy_detail': Pregnancy.objects.get(pk=patient_other_illness.pregnancy_id).desc if patient_other_illness.pregnancy_id is not None else None,
    })
    upcoming = None
    appointments_obj = Appointment.objects.filter(patient=patient_extra).order_by("-begin")
    appointments = []
    number = 1
    for appointment_obj in appointments_obj:
        if appointment_obj.upcoming():
            upcoming = {
                'appointment': appointment_obj,
                'service': Service_translation.objects.get(
                    service__pk=appointment_obj.service_id,
                    language__pk=dentist.language_id
                )
            }
        appointments.append({
            'appointment': appointment_obj,
            'dentist': User_translation.objects.get(
                dentist__pk=appointment_obj.dentist_id,
                language__pk=dentist.language_id
            ),
            'number': number,
            'service': Service.objects.get(pk=appointment_obj.service_id),
            'service_translation': Service_translation.objects.get(
                service__pk=appointment_obj.service_id,
                language__pk=dentist.language_id
            )
        })
        number += 1
    process_photos = Process_photo.objects.filter(patient=patient_extra)
    if len(process_photos) > 1:
        counter = range(len(process_photos))
        process_photo = process_photos[0]
        process_photos = process_photos[1:]
    elif len(process_photos) == 1:
        counter = range(1)
        process_photo = process_photos[0]
        process_photos = None
    else:
        counter = 0
        process_photo = None
        process_photos = None
    return render(request, "patient/patient.html", {
        'dentist': dentist,
        'notifications': notifications,
        'notifications_count': len(notifications),
        'queries': queries,
        'patient': patient,
        'patient_extra': patient_extra,
        'patient_illness': patient_illness,
        'patient_other_illness': patient_other_illness,
        'userform': userform,
        'illnessform': illnessform,
        'otherillnessform': otherillnessform,
        'upcoming': upcoming,
        'appointments': appointments,
        'process_photos': process_photos,
        'process_photo': process_photo,
        'counter': counter,
        'active_tab': active_tab,
        'year': year,
        'gender': gender
    })


def update(request, id, form):
    if not is_authenticated(request, "dentist"):
        if not is_authenticated(request, "patient"):
            return redirect(f"{global_settings.LOGIN_URL_DENTX}?next={request.path}")
        else:
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        check_language(request, "dentist")
    if request.method == "POST":
        patient = PatientUser.objects.get(pk=id)
        user = User.objects.get(pk=patient.user_id)
        if form == "profile":
            userform = UserForm(request.POST)
            illnessform = IllnessForm(request.POST)
            otherillnessform = OtherIllnessForm(request.POST)
            if userform.is_valid() and illnessform.is_valid() and otherillnessform.is_valid():
                user.first_name = userform.cleaned_data['first_name']
                user.last_name = userform.cleaned_data['last_name']
                patient.gender_id = userform.cleaned_data['gender']
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                patient.birthday = datetime(year, month, day)
                patient.phone_number = userform.cleaned_data['phone_number']
                user.email = userform.cleaned_data['email']
                patient.address = userform.cleaned_data['address']
                user.save()
                patient.save()
                userform = UserForm(request.POST)
                illness = Illness.objects.get(patient=patient)
                if illnessform.cleaned_data['allergy'] == 2:
                    try:
                        allergy = Allergy.objects.get(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                    except:
                        allergy = Allergy.objects.create(
                            value=illnessform.cleaned_data['allergy'],
                            desc=illnessform.cleaned_data['allergy_detail'],
                        )
                else:
                    allergy = Allergy.objects.get(
                        value=illnessform.cleaned_data['allergy'],
                    )
                illness.diabet_id = Diabet.objects.get(value=illnessform.cleaned_data['diabet']).id
                illness.anesthesia_id = Anesthesia.objects.get(value=illnessform.cleaned_data['anesthesia']).id
                illness.hepatitis_id = Hepatitis.objects.get(value=illnessform.cleaned_data['hepatitis']).id
                illness.aids_id = AIDS.objects.get(value=illnessform.cleaned_data['aids']).id
                illness.pressure_id = Pressure.objects.get(value=illnessform.cleaned_data['pressure']).id
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=illnessform.cleaned_data['asthma']).id
                illness.dizziness_id = Dizziness.objects.get(value=illnessform.cleaned_data['dizziness']).id
                illness.save()
                illnessform = IllnessForm(request.POST)
                otherillness = Other_Illness.objects.get(patient=patient)
                if otherillnessform.cleaned_data['medications'] == 2:
                    try:
                        medications = Medications.objects.get(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                    except:
                        medications = Medications.objects.create(
                            value=otherillnessform.cleaned_data['medications'],
                            desc=otherillnessform.cleaned_data['medications_detail'],
                        )
                else:
                    medications = Medications.objects.get(
                        value=otherillnessform.cleaned_data['medications'],
                    )
                if otherillnessform.cleaned_data['pregnancy'] == 2:
                    try:
                        pregnancy = Pregnancy.objects.get(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                    except:
                        pregnancy = Pregnancy.objects.create(
                            value=otherillnessform.cleaned_data['pregnancy'],
                            desc=otherillnessform.cleaned_data['pregnancy_detail'],
                        )
                else:
                    pregnancy = Pregnancy.objects.get(
                        value=otherillnessform.cleaned_data['pregnancy'],
                    )
                otherillness.epilepsy_id = Epilepsy.objects.get(value=otherillnessform.cleaned_data['epilepsy']).id
                otherillness.blood_disease_id = Blood_disease.objects.get(value=otherillnessform.cleaned_data['blood_disease']).id
                otherillness.medications_id = medications.id
                otherillness.stroke_id = Stroke.objects.get(value=otherillnessform.cleaned_data['stroke']).id
                otherillness.heart_attack_id = Heart_attack.objects.get(value=otherillnessform.cleaned_data['heart_attack']).id
                otherillness.oncologic_id = Oncologic.objects.get(value=otherillnessform.cleaned_data['oncologic']).id
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=otherillnessform.cleaned_data['tuberculosis']).id
                otherillness.alcohol_id = Alcohol.objects.get(value=otherillnessform.cleaned_data['alcohol']).id
                otherillness.pregnancy_id = pregnancy.id
                otherillness.save()
                otherillnessform = OtherIllnessForm(request.POST)
                return redirect("dentx:patient", id=id, active_tab="profile")
        elif form == "process-photo":
            process_photo = Process_photo.objects.create(
                image=request.FILES['file'],
                patient=patient
            )
            process_photos = Process_photo.objects.filter(patient=patient)
            if len(process_photos) > 1:
                counter = len(process_photos)
                process_photo = process_photos[0].image.url
                process_photos = [image.image.url for image in process_photos[1:]]
            elif len(process_photos) == 1:
                counter = 1
                process_photo = process_photos[0].image.url
                process_photos = None
            else:
                counter = 0
                process_photo = None
                process_photos = None
            return JsonResponse({
                'process_photos': process_photos,
                'process_photo': process_photo,
                'counter': counter,
            }, safe=False)
        return redirect("dentx:patient", id=id, active_tab="profile")
