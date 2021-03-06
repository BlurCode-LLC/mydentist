from django import forms
from django.utils.translation import ugettext_lazy as _
from mydentist.var import CHOICES


class IllnessForm(forms.Form):

    diabet = forms.IntegerField(
        label=_("Qand kasalligi"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['diabet']
        ),
        localize=True,
    )
    anesthesia = forms.IntegerField(
        label=_("Nechi marta narkoz qo'llanilgan?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['anesthesia']
        ),
        localize=True,
    )
    hepatitis = forms.IntegerField(
        label=_("Gepatit (B yoki C)"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['hepatitis']
        ),
        localize=True,
    )
    aids = forms.IntegerField(
        label=_("OITS"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['aids']
        ),
        localize=True,
    )
    pressure = forms.IntegerField(
        label=_("Qon bosimi"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['pressure']
        ),
        localize=True,
    )
    allergy = forms.IntegerField(
        label=_("Allergiya"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['allergy']
        ),
        localize=True,
    )
    allergy_detail = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control mt-3 d-none",
                'placeholder': _("Nimaga allergiya borligini yozing")
            }
        ),
        max_length=255,
        required=False
    )
    asthma = forms.IntegerField(
        label=_("Bronxial astma"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['asthma']
        ),
        localize=True,
    )
    dizziness = forms.IntegerField(
        label=_("Bosh aylanishi"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['dizziness']
        ),
        localize=True,
    )
    fainting = forms.IntegerField(
        label=_("Hushdan ketish"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['fainting']
        ),
        localize=True,
    )


class OtherIllnessForm(forms.Form):
    
    epilepsy = forms.IntegerField(
        label=_("Epilepsiya (tutqanoq)"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['epilepsy']
        ),
        localize=True,
        required=False
    )
    medications = forms.IntegerField(
        label=_("Doimiy qabul qiladigan dorilar"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['medications']
        ),
        localize=True,
        required=False
    )
    medications_detail = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control mt-3 d-none",
                'placeholder': _("Doimiy dorilaringizni yozing")
            }
        ),
        max_length=255,
        required=False
    )
    stroke = forms.IntegerField(
        label=_("Insult bo'lganmisiz?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['stroke']
        ),
        localize=True,
        required=False
    )
    heart_attack = forms.IntegerField(
        label=_("Infarkt bo'lganmisiz?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['heart_attack']
        ),
        localize=True,
        required=False
    )
    oncologic = forms.IntegerField(
        label=_("Onkologik kasallik (o'sma - ??????)"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['oncologic']
        ),
        localize=True,
        required=False
    )
    tuberculosis = forms.IntegerField(
        label=_("Tuberkuloz"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['tuberculosis']
        ),
        localize=True,
        required=False
    )
    alcohol = forms.IntegerField(
        label=_("Alkogol iste'mol qilasizmi?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['alcohol']
        ),
        localize=True,
        required=False
    )
    pregnancy = forms.IntegerField(
        label=_("Homiladormisiz?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['pregnancy']
        ),
        localize=True,
        required=False
    )
    pregnancy_detail = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control mt-3 d-none",
                'placeholder': _("Nechi oyligini yozing")
            }
        ),
        max_length=255,
        required=False
    )
    breastfeeding = forms.IntegerField(
        label=_("Emizasizmi?"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['breastfeeding']
        ),
        localize=True,
        required=False
    )
