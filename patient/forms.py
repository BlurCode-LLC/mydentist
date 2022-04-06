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
                'pattern': "[(]{1}[\d]{2})[)]{1} [\d]{3}-[\d]{2}-[\d]{2}]",
                'placeholder': _("(XX) XXX-XX-XX"),
                'min-length': "14",
                'max-length': "14"
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
                ('2', "Русский"),
                ('3', "English")
            ]
        )
    )


class PatientForm(forms.Form):
    
    name = forms.CharField(
        label=_("Bemor"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
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
                'type': "tel",
                'pattern': "[(]{1}[\d]{2})[)]{1} [\d]{3}-[\d]{2}-[\d]{2}]",
                'placeholder': _("(XX) XXX-XX-XX"),
                'min-length': "14",
                'max-length': "14"
            }
        ),
        localize=True
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


class CodeForm(forms.Form):

    key = forms.IntegerField(
        label=_("Kod"),
        widget=forms.NumberInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Kodni kiriting"),
            }
        ),
        localize=True,
        min_value=100000,
        max_value=999999
    )

