from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from mydentist.var import *


class QueryForm(forms.Form):

    reason_name = forms.CharField(
        label=_("Borish sababi"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("Sabablar"),
                'rows': 3
            }
        ),
        localize=True
    )
    reason = forms.CharField(
        label=_("Sabablarni tanlang"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            # choices=CHOICES['reason']
        ),
        localize=True,
        required=False
    )
    reason_detail = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Sababini kiriting")
            }
        ),
        required=False
    )
    comment = forms.CharField(
        label=_("Tish shifokoriga izohlar"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("Izohlaringizni kiriting")
            }
        ),
        localize=True,
        required=False
    )


class UserForm(forms.Form):

    first_name = forms.CharField(
        label=_("Ism"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Ismingiz")
            }
        ),
        max_length=150,
        localize=True
    )
    last_name = forms.CharField(
        label=_("Familiya"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Familiyangiz")
            }
        ),
        max_length=150,
        localize=True
    )
    gender = forms.CharField(
        label=_("Jins"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['gender']
        )
    )
    birth_year = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "year_holder",
                'value': datetime.today().year
            }
        ),
        localize=True
    )
    birth_month = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "month_holder",
                'value': MONTHS[datetime.today().month - 1]
            }
        ),
        localize=True
    )
    birth_day = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "day_holder",
                'value': datetime.today().day
            }
        ),
        localize=True
    )
    phone_number = forms.CharField(
        label=_("Telefon raqam"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Telefon raqamingiz")
            }
        ),
        max_length=100,
        localize=True
    )
    email = forms.EmailField(
        label=_("Elektron manzil"),
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Elektron pochtangiz")
            }
        ),
        localize=True,
        required=False
    )


class ClinicForm(forms.Form):

    clinic_name_uz = forms.CharField(
        label=_("Shifoxona nomi (o'zbekchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Shifoxona nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    clinic_name_ru = forms.CharField(
        label=_("Shifoxona nomi (ruschada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Shifoxona nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    clinic_name_en = forms.CharField(
        label=_("Shifoxona nomi (inglizchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Shifoxona nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    address_uz = forms.CharField(
        label=_("Manzil (o'zbekchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Manzil")
            }
        ),
        max_length=150,
        localize=True
    )
    address_ru = forms.CharField(
        label=_("Manzil (ruschada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Manzil")
            }
        ),
        max_length=150,
        localize=True
    )
    address_en = forms.CharField(
        label=_("Manzil (inglizchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Manzil")
            }
        ),
        max_length=150,
        localize=True
    )
    orientir_uz = forms.CharField(
        label=_("Mo'ljal (o'zbekchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Mo'ljal")
            }
        ),
        max_length=150,
        localize=True,
        required=False
    )
    orientir_ru = forms.CharField(
        label=_("Mo'ljal (ruschada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Mo'ljal")
            }
        ),
        max_length=150,
        localize=True,
        required=False
    )
    orientir_en = forms.CharField(
        label=_("Mo'ljal (inglizchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Mo'ljal")
            }
        ),
        max_length=150,
        localize=True,
        required=False
    )
    latitude = forms.CharField(
        label=_("Kenglik"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
    longitude = forms.CharField(
        label=_("Uzunlik"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
            }
        ),
        localize=True
    )
    region = forms.CharField(
        label=_("Hudud"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['regions']
        )
    )

class WorkTimeForm(forms.Form):
    
    work_days = forms.ChoiceField(
        label=_("Ish kuni"),
        widget=forms.RadioSelect(
            attrs={
                'class': "form-switch"
            }
        ),
        choices=(
            (6, _("6-kunlik ish")),
            (7, _("7-kunlik ish"))
        )
    )
    worktime_begin = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "worktime_begin_holder",
                'value': "9:00"
            }
        ),
        localize=True
    )
    worktime_end = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "worktime_end_holder",
                'value': "18:00"
            }
        ),
        localize=True
    )
    no_queue = forms.BooleanField(
        label=_("Navbatsiz"),
        widget=forms.CheckboxInput(
            attrs={
                'class': "form-check-input"
            }
        ),
        localize=True,
        required=False
    )


class ServiceForm(forms.Form):

    name_uz = forms.CharField(
        label=_("Xizmat nomi (o'zbekchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control wid",
                'placeholder': _("Xizmat nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    name_ru = forms.CharField(
        label=_("Xizmat nomi (ruschada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control wid",
                'placeholder': _("Xizmat nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    name_en = forms.CharField(
        label=_("Xizmat nomi (inglizchada)"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control wid",
                'placeholder': _("Xizmat nomi")
            }
        ),
        max_length=150,
        localize=True
    )
    duration = forms.CharField(
        label=_("Xizmat davomiyligi"),
        widget=forms.Select(
            attrs={
                'class': "form-select wid"
            },
            choices=CHOICES['duration']
        )
    )
    price = forms.IntegerField(
        label=_("Xizmat narxi"),
        widget=forms.NumberInput(
            attrs={
                'class': "form-control wid"
            }
        ),
        localize=True
    )
