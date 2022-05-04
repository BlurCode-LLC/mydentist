from datetime import datetime
from random import randint
from django.conf import settings as global_settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import get_language, ugettext_lazy as _
from baseapp.models import Language, Gender
from dentist.models import User as DentistUser
from illness.models import *
from illness.forms import *
from patient.models import Key, User as PatientUser, Illness, Other_Illness
from patient.forms import *
from mydentist.handler import *
from mydentist.var import *
from .models import *
from .forms import *
from .tokens import reset_password_token


def register(request):
    if is_authenticated(request, "patient") or is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.method == "POST":
        print(request.POST)
        userform = UserForm(request.POST)
        passwordform = PasswordForm(request.POST)
        illnessform = IllnessForm(request.POST)
        otherillnessform = OtherIllnessForm(request.POST)
        if userform.is_valid() and passwordform.is_valid() and illnessform.is_valid() and otherillnessform.is_valid():
            if passwordform.cleaned_data['password'] == passwordform.cleaned_data['password_confirm']:
                file_path = global_settings.PROJECT_DIR / "last_id.txt"
                with open(file_path, "r") as file:
                    id = int(file.read()) + 1
                with open(file_path, "w") as file:
                    file.write(str(id))
                id = f"{id:07d}"
                user = User.objects.create_user(
                    f"user{id}",
                    email=userform.cleaned_data['email'],
                    password=passwordform.cleaned_data['password'],
                    first_name=userform.cleaned_data['first_name'],
                    last_name=userform.cleaned_data['last_name']
                )
                year = int(userform.cleaned_data['birth_year'])
                month = MONTHS.index(userform.cleaned_data['birth_month']) + 1
                day = int(userform.cleaned_data['birth_day'])
                try:
                    user_extra = PatientUser.objects.create(
                        user=user,
                        phone_number=userform.cleaned_data['phone_number'],
                        address=userform.cleaned_data['address'],
                        birthday=datetime(year, month, day),
                        image="patients/photos/default.png",
                        language=Language.objects.get(name=get_language()),
                        gender=Gender.objects.get(pk=userform.cleaned_data['gender'])
                    )
                except:
                    return render(request, "login/register.html", {
                        'userform': userform,
                        'passwordform': passwordform,
                        'illnessform': illnessform,
                        'otherillnessform': otherillnessform,
                        'error_message': _("Bu raqam ostida foydalanuvchi mavjud")
                    })
                key = Key.objects.create(
                    patient=user_extra,
                    key=randint(100000, 999999)
                )
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
                illness = Illness.objects.get(patient=user_extra)
                illness.diabet_id = Diabet.objects.get(value=illnessform.cleaned_data['diabet']).id
                illness.anesthesia_id = Anesthesia.objects.get(value=illnessform.cleaned_data['anesthesia']).id
                illness.hepatitis_id = Hepatitis.objects.get(value=illnessform.cleaned_data['hepatitis']).id
                illness.aids_id = AIDS.objects.get(value=illnessform.cleaned_data['aids']).id
                illness.pressure_id = Pressure.objects.get(value=illnessform.cleaned_data['pressure']).id
                illness.allergy_id = allergy.id
                illness.asthma_id = Asthma.objects.get(value=illnessform.cleaned_data['asthma']).id
                illness.dizziness_id = Dizziness.objects.get(value=illnessform.cleaned_data['dizziness']).id
                illness.save()
                otherillness = Other_Illness.objects.get(patient=user_extra)
                otherillness.epilepsy_id = Epilepsy.objects.get(value=otherillnessform.cleaned_data['epilepsy']).id if otherillnessform.cleaned_data.get('epilepsy') is not None else None
                otherillness.blood_disease_id = Blood_disease.objects.get(value=otherillnessform.cleaned_data['blood_disease']).id if otherillnessform.cleaned_data.get('blood_disease') is not None else None
                if otherillnessform.cleaned_data.get('medications') is not None:
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
                    otherillness.medications_id = medications.id
                else:
                    otherillness.medications_id = None
                otherillness.stroke_id = Stroke.objects.get(value=otherillnessform.cleaned_data['stroke']).id if otherillnessform.cleaned_data.get('stroke') is not None else None
                otherillness.heart_attack_id = Heart_attack.objects.get(value=otherillnessform.cleaned_data['heart_attack']).id if otherillnessform.cleaned_data.get('heart_attack') is not None else None
                otherillness.oncologic_id = Oncologic.objects.get(value=otherillnessform.cleaned_data['oncologic']).id if otherillnessform.cleaned_data.get('oncologic') is not None else None
                otherillness.tuberculosis_id = Tuberculosis.objects.get(value=otherillnessform.cleaned_data['tuberculosis']).id if otherillnessform.cleaned_data.get('tuberculosis') is not None else None
                otherillness.alcohol_id = Alcohol.objects.get(value=otherillnessform.cleaned_data['alcohol']).id if otherillnessform.cleaned_data.get('alcohol') is not None else None
                if otherillnessform.cleaned_data.get('pregnancy') is not None:
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
                    otherillness.pregnancy_id = pregnancy.id
                else:
                    otherillness.pregnancy_id = None
                otherillness.save()
                user = authenticate(
                    request,
                    username=user.username,
                    password=passwordform.cleaned_data['password']
                )
                login(request, user)
                language = Language.objects.get(pk=user_extra.language_id).name
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                request.session[user.get_username()] = user.get_username()
                return redirect("baseapp:index")
            else:
                return render(request, "login/register.html", {
                    'userform': userform,
                    'passwordform': passwordform,
                    'illnessform': illnessform,
                    'otherillnessform': otherillnessform,
                    'error_message': _("Parollar to'g'ri kemayapti")
                })
        else:
            return render(request, "login/register.html", {
                'userform': userform,
                'passwordform': passwordform,
                'illnessform': illnessform,
                'otherillnessform': otherillnessform,
                'error_message': None
            })
    else:
        userform = UserForm()
        passwordform = PasswordForm()
        illnessform = IllnessForm()
        otherillnessform = OtherIllnessForm()
        return render(request, "login/register.html", {
            'userform': userform,
            'passwordform': passwordform,
            'illnessform': illnessform,
            'otherillnessform': otherillnessform,
            'error_message': None
        })


def sign_in(request):
    if is_authenticated(request, "patient") or is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            try:
                user_check = User.objects.get(email=request.POST['email'])
                user = authenticate(
                    request,
                    username=user_check.username,
                    password=loginform.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    user_extra = PatientUser.objects.get(user=user)
                    language = Language.objects.get(pk=user_extra.language_id).name
                    translation.activate(language)
                    request.session[translation.LANGUAGE_SESSION_KEY] = language
                    request.session[user.get_username()] = user.get_username()
                    if 'next' in request.POST:
                        return redirect(request.POST['next'])
                    else:
                        return redirect("baseapp:index")
                else:
                    return render(request, "login/login.html", {
                        'loginform': loginform,
                        'error_message': _("Xato parol")
                    })
            except:
                try:
                    user_check = PatientUser.objects.get(phone_number=loginform.cleaned_data['email'])
                    user_check = User.objects.get(pk=user_check.user_id)
                    user = authenticate(
                        request,
                        username=user_check.username,
                        password=request.POST['password']
                    )
                    if user is not None:
                        login(request, user)
                        user_extra = PatientUser.objects.get(user=user)
                        language = Language.objects.get(pk=user_extra.language_id).name
                        translation.activate(language)
                        request.session[translation.LANGUAGE_SESSION_KEY] = language
                        request.session[user.get_username()] = user.get_username()
                        if 'next' in request.POST:
                            return redirect(request.POST['next'])
                        else:
                            return redirect("baseapp:index")
                    else:
                        return render(request, "login/login.html", {
                            'loginform': loginform,
                            'error_message': _("Xato parol")
                        })
                except:
                    return render(request, "login/login.html", {
                        'loginform': loginform,
                        'error_message': _("Xato telefon raqam")
                    })
        else:
            return render(request, "login/login.html", {
                'loginform': loginform,
                'error_message': None
            })
    else:
        loginform = LoginForm()
        return render(request, "login/login.html", {
            'loginform': loginform,
            'error_message': None
        })


def sign_out(request):
    if is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.user.username in request.session:
        del request.session[request.user.username]
    logout(request)
    return redirect("login:login")


def password_reset(request):
    if is_authenticated(request, "patient") or is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.method == "POST":
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except:
                emailform = EmailForm()
                return render(request, "login/password_reset.html", {
                    'message': _("Foydalanuvchi topilmadi"),
                    'emailform': emailform
                })
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
                return redirect("login:password_reset_done")
    else:
        emailform = EmailForm()
        return render(request, "login/password_reset.html", {
            'message': None,
            'emailform': emailform
        })


def password_reset_done(request):
    if is_authenticated(request, "patient") or is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return render(request, "login/password_reset_sent.html")


def reset(request, uidb64, token):
    try:
        user = User.objects.get(username=force_str(urlsafe_base64_decode(uidb64)))
        is_token_correct = reset_password_token.check_token(user, token)
        if is_token_correct:
            try:
                password_reset = PasswordReset.objects.get(
                    email=user.email,
                    uidb64=uidb64,
                    token=token
                )
                if password_reset.is_active:
                    if request.method == "POST":
                        passwordform = PasswordForm(request.POST)
                        if passwordform.is_valid():
                            if passwordform.cleaned_data['password'] == passwordform.cleaned_data['password_confirm']:
                                user.set_password(passwordform.cleaned_data['password'])
                                user.save()
                                password_reset.is_active = False
                                password_reset.save()
                                return redirect("login:password_reset_complete")
                            else:
                                passwordform = PasswordForm(request.POST)
                                return render(request, "login/password_reset_form.html", {
                                    'passwordform': passwordform,
                                    'error_message': _("Parollar mos kelmayapti")
                                })
                        else:
                            passwordform = PasswordForm(request.POST)
                            return render(request, "login/password_reset_form.html", {
                                'passwordform': passwordform,
                                'error_message': None
                            })
                    else:
                        passwordform = PasswordForm()
                        return render(request, "login/password_reset_form.html", {
                            'passwordform': passwordform,
                            'error_message': None
                        })
                else:
                    raise Http404(_("Havolani muddati yakunlandi"))
            except:
                raise Http404(_("Havolani muddati yakunlandi"))
        else:
            raise Http404(_("Havolani muddati yakunlandi"))
    except:
        raise Http404(_("Havolani muddati yakunlandi"))


def reset_done(request):
    if is_authenticated(request, "patient") or is_authenticated(request, "dentist"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return render(request, "login/password_reset_done.html")


def dentx_login(request):
    if is_authenticated(request, "dentist") or is_authenticated(request, "patient"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.method == "POST":
        loginform = DentXLoginForm(request.POST)
        if loginform.is_valid():
            user = authenticate(
                request,
                username=loginform.cleaned_data['username'],
                password=loginform.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                try:
                    dentist_extra = DentistUser.objects.get(user=user)
                except:
                    raise PermissionDenied()
                    # return HttpResponseForbidden(_("Ushbu bo'limga faqat tish shifokorlari kirishi mumkin"))
                language = Language.objects.get(pk=dentist_extra.language_id).name
                translation.activate(language)
                request.session[translation.LANGUAGE_SESSION_KEY] = language
                request.session[user.get_username()] = user.get_username()
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    return redirect("dentx:appointments")
            else:
                try:
                    user_check = User.objects.get(email=loginform.cleaned_data['username'])
                    user = authenticate(
                        request,
                        username=user_check.username,
                        password=loginform.cleaned_data['password']
                    )
                    if user is not None:
                        raise PermissionDenied()
                except:
                    pass
                return render(request, "login/dentx_login.html", {
                    'loginform': loginform,
                    'error_message': _("Noto'g'ri login yoki parol")
                })
        else:
            loginform = DentXLoginForm()
            return render(request, "login/dentx_login.html", {
                'loginform': loginform,
                'error_message': None
            })
    else:
        loginform = DentXLoginForm()
        return render(request, "login/dentx_login.html", {
            'loginform': loginform,
            'error_message': None
        })


def dentx_logout(request):
    if is_authenticated(request, "patient"):
        return redirect(request.META.get("HTTP_REFERER", "/"))
    if request.user.username in request.session:
        del request.session[request.user.username]
    logout(request)
    return redirect("dentx:login")
