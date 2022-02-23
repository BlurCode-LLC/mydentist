from django import forms
from django.utils.translation import ugettext_lazy as _
from mydentist.var import CHOICES


class AppointmentForm(forms.Form):
    
    service = forms.CharField(
        label=_("Xizmat"),
        widget=forms.Select(
            attrs={
                'class': "form-select wid"
            }
        ),
        localize=True
    )
    begin_day = forms.CharField(
        widget=forms.HiddenInput()
    )
    begin_time = forms.CharField(
        label=_("Boshlanish vaqti"),
        widget=forms.Select(
            attrs={
                'class': "form-select wid"
            }
        )
    )
    duration = forms.CharField(
        label=_("Davomiyligi"),
        widget=forms.Select(
            attrs={
                'class': "form-select wid"
            },
            choices=CHOICES['duration']
        )
    )
    comment = forms.CharField(
        label=_("Eslatma"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control w-100"
            }
        ),
        required=False
    )

