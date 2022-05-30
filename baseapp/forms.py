from django import forms
from django.utils.translation import ugettext_lazy as _, get_language


class SearchForm(forms.Form):

    service = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'value': 1
            }
        )
    )
    region = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'value': 1
            }
        )
    )

class GeoForm(forms.Form):
    
    latitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
