from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from dashboard.models import Specialist

# class SpecialistForm(forms.Form):
#     user = forms.CharField()

class SpecialistForm(ModelForm):
    CHOICES_C = (
        (1, 'Lima'),
    )
    CHOICES_D = (
        (1, 'Lima'),
    )
    CHOICES_P = (
        (1, 'Surco'),
    )

    category    = forms.CharField(widget=forms.Select(),required=True,label=_('category').title())
    department  = forms.CharField(widget=forms.Select(choices=CHOICES_C),required=True,label=_('department').title())
    province    = forms.CharField(widget=forms.Select(choices=CHOICES_D),required=True,label=_('province').title())
    district    = forms.CharField(widget=forms.Select(choices=CHOICES_P),required=True,label=_('district').title())
    street      = forms.CharField(required=True,label=_('street').title())
    
    confirm_password = forms.CharField(widget=forms.PasswordInput,label=_('confirm password').title())
    widgets = {
        'confirm_password': forms.PasswordInput(),
    }


    def __init__(self,initial=None, categories=None,departments=None,provinces=None,districts=None,form_edit=None, *args, **kwargs):
        super(SpecialistForm, self).__init__(initial=initial,*args, **kwargs)

        if categories:
            self.fields['category'].widget.choices      = [('','')] + [(l['id'], l['name']) for l in categories]

        if departments:
            self.fields['department'].widget.choices    = [('','')] + [(l['id'], l['name']) for l in departments]

        if provinces:
            self.fields['province'].widget.choices      = [('','')] + [(l['id'], l['name']) for l in provinces]

        if districts:
            self.fields['district'].widget.choices      = [('','')] + [(l['id'], l['name']) for l in districts]


        if form_edit:
            self.fields.pop('password')
            self.fields.pop('confirm_password')
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['readonly'] = True
            

        
        # Algoritmo para poder extraer subitem en el initial del form
        # este algoritmo se realiza mas que todo para solventar el envio
        # de data anidad desde la API RESTFULL
        if initial:
            for item in initial:
                if type(initial[item]) is dict:
                    for key in initial[item]:
                        if key in self.fields:
                            self.fields[key].initial = initial[item][key]


    def clean(self):
        cleaned_data = super(SpecialistForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                _("Password and confirm_password does not match")
            )


    def add_error_custom(self,add_errors=None):
        if add_errors:  # errores retornados por terceros
            for key in add_errors:
                if key in self.fields and add_errors[key] and type(add_errors[key]) is list:
                    print("soy un %##### LIST")
                    print("------------------------------------")
                    self.add_error(key,add_errors[key])
                elif type(key) is list:
                    print("soy un #$#$ DICT")
                    print("------------------------------------")
                    for item in key:
                        if item and item in self.fields:
                            self.add_error(item,key[item])
    

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
        model   = Specialist
        fields  = ['payment_per_answer','username','nick','password','first_name','last_name','email_exact','telephone','cellphone','document_type','document_number','ruc', 'business_name','type_specialist']
        labels  = {
            'username'          : _('username').title(),
            'nick'              : _('nick').title(),
            'password'          : _('password').title(),
            'first_name'        : _('firstname').title(),
            'last_name'         : _('lastname').title(),
            'email_exact'       : _('email').title(),
            'telephone'         : _('telephone').title(),
            'cellphone'         : _('cellphone').title(),
            'document_type'     : _('document type').title(),
            'document_number'   : _('document number').title(),
            'ruc'               : _('RUC').title(),
            'business_name'    : _('business name').title(),
            'type_specialist'   : _('type specialist').title(),
        }