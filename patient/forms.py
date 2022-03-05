from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from mydentist.var import *


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
                'type': "tel",
                'pattern': "([0-9]{2}) [0-9]{3}-[0-9]{2}-[0-9]{2}",
                'placeholder': _("(XX) XXX-XX-XX")
            }
        ),
        max_length=20,
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
    address = forms.CharField(
        label=_("Manzil"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Manzilingiz")
            }
        ),
        max_length=150,
        localize=True
    )


class LanguageForm(forms.Form):
    
    language = forms.CharField(
        label=_("Til"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=[
                ('1', "O'zbekcha"),
                ('2', "Русский")
            ]
        )
    )


class PatientForm(forms.Form):
    
    name = forms.CharField(
        label=_("Bemor"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control mb-3",
                'placeholder': _("Bemor FIOsi"),
            }
        ),
        localize=True
    )
    phone_number = forms.CharField(
        label=_("Telefon raqami"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control wid",
                'placeholder': _("+9989XXXXXXXX"),
            }
        ),
        localize=True
    )
    birthday = forms.CharField(
        label=_("Tugilgan sana"),
        widget=forms.DateInput(
            attrs={
                'class': "form-control wid",
                'type': "date",
            }
        ),
        localize=True
    )
    gender = forms.CharField(
        label=_("Jins"),
        widget=forms.RadioSelect(
            attrs={
                'class': "form-switch m-1",
            },
            choices=CHOICES['gender']
        )
    )
    address = forms.CharField(
        label=_("Manzil"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control w-100",
                'placeholder': _("Manzilni kiriting"),
            }
        ),
        localize=True
    )

