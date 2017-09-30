from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from dashboard.models import Specialist

# class SpecialistForm(forms.Form):
#     user = forms.CharField()

class SpecialistForm(ModelForm):

    # category 	= forms.ChoiceField(required=False,label=_('category').title())
    # department  = forms.ChoiceField(required=False,label=_('department').title())
    # province    = forms.ChoiceField(required=False,label=_('province').title())
    # district	= forms.ChoiceField(required=False,label=_('district').title())

    class Meta:
        model   = Specialist
        fields  = ['first_name','last_name','email_exact','telephone','cellphone','document_type','document_number','ruc', 'bussiness_name','type_specialist']
        labels  = {
            'email_exact': _('email').title(),
            'ruc': 'RUC',
        }