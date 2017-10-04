from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from dashboard.models import Specialist

# class SpecialistForm(forms.Form):
#     user = forms.CharField()

class SpecialistForm(ModelForm):
    
    category    = forms.CharField(widget=forms.Select(),required=False,label=_('category').title())
    department  = forms.CharField(widget=forms.Select(),required=False,label=_('department').title())
    province    = forms.CharField(widget=forms.Select(),required=False,label=_('province').title())
    district    = forms.CharField(widget=forms.Select(),required=False,label=_('district').title())
    


    def __init__(self, categories=None,departments=None,provinces=None,districts=None, *args, **kwargs):
        super(SpecialistForm, self).__init__(*args, **kwargs)

        if categories:
            self.fields['category'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in categories]

        if departments:
            self.fields['department'].widget.choices    = [('','')] + [(l['name'], l['name']) for l in departments]

        if provinces:
            self.fields['province'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in provinces]

        if districts:
            self.fields['district'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in districts]


    class Meta:
        model   = Specialist
        fields  = ['username','nick','password','first_name','last_name','email_exact','telephone','cellphone','document_type','document_number','ruc', 'bussiness_name','type_specialist']
        labels  = {
            'email_exact': _('email').title(),
            'ruc': 'RUC',
        }