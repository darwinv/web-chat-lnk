from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from dashboard.models import Specialist

from api.connection import api

from django.contrib.admin.widgets import AdminDateWidget

class FilterForm(forms.Form):
    """
    Clase creada para estandarizar las caracteristicas de los filtros
    Al heredar de esta clase ya se incluira el envio de paginacion,
    por defecto ningun valor sera requerido, si hereda de esta clase
    a menos que sea definido como requerido
    """
    page = forms.CharField()
    showFilters = False


    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False  # Los filtros no se validan, por eso siempre para esta clase no seran requeridos

    def clean(self):
        super(forms.Form, self).clean()
        data = self.cleaned_data

        for field in data:  # Los filtros vacios seran seteados en None
            if not data[field] or data[field] == '':
                self.cleaned_data[field] = None
            elif field!='page' :  # Ignoramos la paginacion para el atributo Mostrar Filtros
                self.showFilters = True

        return self.cleaned_data


class SellerFormFilters(FilterForm):
    """
    Clase creada para filtrar el listado de vendedores
    """
    first_name = forms.CharField(label=_('first name').title())
    last_name = forms.CharField(label=_('last name').title())
    ruc = forms.CharField(label=_('RUC'))
    email_exact = forms.CharField(label=_('mail').title())

    count_plans_seller = forms.IntegerField(label=_('number of plans sold greater than').title())
    count_queries_seller = forms.IntegerField(label=_('number of queries sold greater than').title())



class SpecialistForm(ModelForm):
    # Data fake
    CHOICES_C = (
        (1, 'Lima'),
    )
    CHOICES_D = (
        (1, 'Lima'),
    )
    CHOICES_P = (
        (1, 'Surco'),
    )

    category = forms.CharField(widget=forms.Select(), required=True, label=_('category').title())
    department = forms.CharField(widget=forms.Select(choices=CHOICES_C), required=True, label=_('department').title())
    province = forms.CharField(widget=forms.Select(choices=CHOICES_D), required=True, label=_('province').title())
    district = forms.CharField(widget=forms.Select(choices=CHOICES_P), required=True, label=_('district').title())
    street = forms.CharField(required=True, label=_('street').title())
    photo = forms.FileField(required=False, label=_('upload a photo').title(), widget=forms.TextInput(
        attrs={'class': 'sr-only', 'id': 'inputFile', 'accept': '.jpg,.jpeg,.png,.gif,.bmp,.tiff', 'type': 'file'}, ))

    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_('confirm password').title())

    widgets = {
        'confirm_password': forms.PasswordInput(),
    }

    def __init__(self, initial=None, categories=None, departments=None, provinces=None, districts=None, form_edit=None,
                 *args, **kwargs):
        super(SpecialistForm, self).__init__(initial=initial, *args, **kwargs)

        if categories:
            self.fields['category'].widget.choices = [('', '')] + [(l['id'], l['name']) for l in categories]

        if departments:
            self.fields['department'].widget.choices = [('', '')] + [(l['id'], l['name']) for l in departments]

        if provinces:
            self.fields['province'].widget.choices = [('', '')] + [(l['id'], l['name']) for l in provinces]

        if districts:
            self.fields['district'].widget.choices = [('', '')] + [(l['id'], l['name']) for l in districts]

        if form_edit:
            self.fields.pop('password')
            self.fields.pop('confirm_password')
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['readonly'] = True

        # Algoritmo para poder extraer subitem en el initial del form
        # este algoritmo se realiza mas que todo para solventar el envio
        # de data anidada desde la API RESTFULL
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
                _("Password and confirm password does not match")
            )

    def add_error_custom(self, add_errors=None):        
        """
        Funcion creada para agregar errores, posteriormente a las validaciones
        hechas por la clase Form
        """
        if add_errors:  # errores retornados por terceros
            for key in add_errors:
                if key in self.fields and add_errors[key] and type(add_errors[key]) is list:
                    self.add_error(key, add_errors[key])
                elif type(key) is list:
                    for item in key:
                        if item and item in self.fields:
                            self.add_error(item, key[item])

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
        model = Specialist
        fields = ['payment_per_answer', 'username', 'nick', 'password', 'first_name', 'last_name', 'email_exact',
                  'telephone', 'cellphone', 'document_type', 'document_number', 'ruc', 'business_name',
                  'type_specialist']
        labels = {
            'username': _('username').title(),
            'nick': _('nick').title(),
            'password': _('password').title(),
            'first_name': _('first name').title(),
            'last_name': _('last name').title(),
            'email_exact': _('email').title(),
            'telephone': _('telephone').title(),
            'cellphone': _('cellphone').title(),
            'document_type': _('document type').title(),
            'document_number': _('document number').title(),
            'ruc': _('RUC').title(),
            'business_name': _('business name').title(),
            'type_specialist': _('type specialist').title(),
            'payment_per_answer': _('payment per answer').title(),
        }



"""
Reportes de estado de cuenta
"""

class AccountStatus(FilterForm):
    """
    Clase creada para filtrar estados de cuenta
    """
    from_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }),label=_('from').title())
    until_date = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }),label=_('until').title())

    


class AccountStatusSellerFormFilters(AccountStatus):
    """
    Formulario para filtrar estados de cuenta por vendedor
    """
    seller = forms.CharField(widget=forms.Select(), required=True, label=_('seller').title())
    show_sum_column = forms.BooleanField(label=_('Show Total').title())


    def __init__(self, token=None, *args, **kwargs):
        super(AccountStatusSellerFormFilters, self).__init__(*args, **kwargs)
        ObjApi = api()

        # Traer vendedores directamente desde la api
        # y actualizamos los options del select
        # "?page_size=0" trae un listado, ignorando la paginacion
        data = ObjApi.get(slug='sellers/?page_size=0', token=token) 
        
        if type(data) is list:
            self.fields['seller'].widget.choices = [('', '')] + [(l['id'], l['first_name']+' '+l['last_name']) for l in data]