from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from dashboard.models import Specialist

# class SpecialistForm(forms.Form):
#     user = forms.CharField()

class SpecialistForm(ModelForm):
    
    category    = forms.CharField(widget=forms.Select(),required=True,label=_('category').title())
    department  = forms.CharField(widget=forms.Select(),required=False,label=_('department').title())
    province    = forms.CharField(widget=forms.Select(),required=False,label=_('province').title())
    district    = forms.CharField(widget=forms.Select(),required=False,label=_('district').title())
    street      = forms.CharField(required=False,label=_('street').title())
    


    def __init__(self, categories=None,departments=None,provinces=None,districts=None,form_edit=None, *args, **kwargs):
        super(SpecialistForm, self).__init__(*args, **kwargs)

        if categories:
            self.fields['category'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in categories]

        if departments:
            self.fields['department'].widget.choices    = [('','')] + [(l['name'], l['name']) for l in departments]

        if provinces:
            self.fields['province'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in provinces]

        if districts:
            self.fields['district'].widget.choices      = [('','')] + [(l['name'], l['name']) for l in districts]


        if form_edit:
            self.fields.pop('password')

    def add_error_custom(self,add_errors=None):
        if add_errors:  # errores retornados por terceros
            for key in add_errors:
                if key in self.fields and key in add_errors and add_errors[key] and type(add_errors[key]) is list:  # Si existe esa llave en los campos de este formulario
                    for msg in add_errors[key]:
                        self.add_error(key,_(msg))  # creamos un segundo ciclo para poder llamar a _("String")
    

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
        model   = Specialist
        fields  = ['payment_per_answer','username','nick','password','first_name','last_name','email_exact','telephone','cellphone','document_type','document_number','ruc', 'bussiness_name','type_specialist']
        labels  = {
            'email_exact': _('email').title(),
            'ruc': 'RUC',
        }