"""Formularios."""
from django import forms
from django.forms import ModelForm

from api.models import Specialist, Seller, Category, Department, Province, District, Countries, Ciiu

from django.utils.translation import ugettext_lazy as _
from api.connection import api
from api.api_choices_models import ChoicesAPI as Ch

# from dashboard.tools import capitalize as cap

class FilterForm(forms.Form):
    """
    Clase creada para estandarizar las caracteristicas de los filtros
    Al heredar de esta clase ya se incluira el envio de paginacion,
    por defecto ningun valor sera requerido, si hereda de esta clase
    a menos que sea definido como requerido
    """
    page = forms.CharField(required=False)
    showFilters = False

    def __init__(self, *args):
        super(FilterForm, self).__init__(*args)

        # for field in self.fields:
        #     self.fields[field].required = False  # Los filtros no se validan, por eso siempre para esta clase no seran requeridos

    def clean(self):
        super(FilterForm, self).clean()
        data = self.cleaned_data

        for field in data:  # Los filtros vacios seran seteados en None
            if not data[field] or data[field] == '':
                self.cleaned_data[field] = None
            elif field!='page' :  # Ignoramos la paginacion para el atributo Mostrar Filtros
                self.showFilters = True

        return self.cleaned_data

class Operations():
    def setAdress(self, initial, fields):
        # Algoritmo para poder extraer subitem en el initial del form
        # este algoritmo se realiza mas que todo para solventar el envio
        # de data anidada desde la API RESTFULL
        if initial:
            for item in initial:
                if type(initial[item]) is dict:
                    for key in initial[item]:
                        if key in fields:
                            fields[key].initial = initial[item][key]
        return fields


class ErrorsFieldsApi(forms.Form):

    def add_error_custom(self, add_errors=None):
        """
        Funcion creada para agregar errores, posteriormente a las validaciones
        hechas por la clase Form
        """
        print(add_errors)
        print("----------------FORM ERRRORS--------------------")
        if add_errors:  # errores retornados por terceros
            if type(add_errors) is dict:
                for key in add_errors:
                    if key in self.fields and add_errors[key] and type(add_errors[key]) is list:
                        self.add_error(key, add_errors[key])
                    elif type(key) is list:
                        for item in key:
                            if item and item in self.fields:
                                self.add_error(item, key[item])
                    elif key == "non_field_errors":
                        self.add_error(None, error=add_errors[key])
            elif type(add_errors) is list:
                for key in add_errors:
                    self.add_error(None, error=key)

class SpecialistForm(ModelForm, ErrorsFieldsApi):
    """
        Formulario para crear especialistas
    """
    select_search = {'data-live-search':'true','class':'selectpicker'}
    first_name = forms.CharField(required=True, max_length=30, label=_('first name'))
    last_name = forms.CharField(required=True, max_length=30, label=_('last name'))
    category = forms.CharField(widget=forms.Select(), required=False, label=_('category'))
    department = forms.CharField(widget=forms.Select(), required=False, label=_('department'))
    province = forms.CharField(widget=forms.Select(), required=False, label=_('province'))
    district = forms.CharField(widget=forms.Select(), required=False, label=_('district'))
    street = forms.CharField(required=False, label=_('street'))
    photo = forms.FileField(required=False, label=_('upload a photo'), widget=forms.TextInput(
        attrs={'class': 'sr-only inputFile', 'id': 'inputFile', 'accept': '.jpg,.jpeg,.png,.gif,.bmp,.tiff', 'type': 'file'}, ))
    img_document_number = forms.FileField(required=False, label=_('upload document'), widget=forms.TextInput(
        attrs={'class': 'sr-only inputFile', 'accept': '.jpg,.jpeg,.png,.gif,.bmp,.tiff', 'type': 'file', 'data-title':'True'}, ))
    nationality = forms.CharField(widget=forms.Select(attrs=select_search), required=True, label=_('nationality'))
    residence_country = forms.CharField(widget=forms.Select(attrs=select_search), required=True, label=_('residence country'))

    foreign_address = forms.CharField(label = _('address'), required=False)
    ruc = forms.CharField(label = _('ruc'), required=False)

    payment_per_answer = forms.FloatField(min_value=0)

    def __init__(self, data=None, initial=None, department=None, province=None, form_edit=None,
            *args, **kwargs):
        super(SpecialistForm, self).__init__(data=data, initial=initial, *args, **kwargs)

        categories = Category.objects.all()
        departments = Department.objects.all()
        countries = Countries.objects.all()

        if categories:
            self.fields['category'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in categories]

        if departments:
            self.fields['department'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in departments]

        if countries:
            self.fields['nationality'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in countries]

        if countries:
            self.fields['residence_country'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in countries]

        if data and 'department' in data and data['department']:
            department = data['department']

        if data and 'province' in data and data['province']:
            province = data['province']

        if department:
            provinces = Province.objects.filter(department_id=department)
            self.fields['province'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in provinces]

        if province:
            districts = District.objects.filter(province_id=province)
            self.fields['district'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in districts]

        # Si se va a editar el especialista, se elimina la contraseña y se bloquea el campo username
        # se comento porque se quito el campo username del form y de las plantillas
        # if form_edit:
        #     self.fields['username'].required = False
        #     self.fields['username'].widget.attrs['readonly'] = True

        self.fields = Operations.setAdress(self, initial, self.fields)

                            # cambiar a clase generica

    class Meta:
        """Meta."""

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
        model = Specialist
        fields = ['nick', 'first_name', 'last_name',
        # fields = ['payment_per_answer', 'nick', 'first_name', 'last_name',
                  'telephone', 'cellphone', 'document_type', 'email_exact',
                  'business_name', 'type_specialist', 'document_number']


class SellerForm(ModelForm, ErrorsFieldsApi):
    """Formulario de Vendedores."""

    select_search = {'data-live-search': 'true', 'class': 'selectpicker'}
    ciiu = forms.CharField(widget=forms.Select(attrs=select_search),
                           required=False, label=_('CIIU'))
    nationality = forms.CharField(widget=forms.Select(attrs=select_search), required=True, label=_('nationality'))
    residence_country = forms.CharField(widget=forms.Select(attrs=select_search), required=True, label=_('residence country'))
    first_name = forms.CharField(required=True, max_length=30, label=_('first name'))
    last_name = forms.CharField(required=True, max_length=30, label=_('last name'))
    department = forms.CharField(widget=forms.Select(), required=False, label=_('department'))
    province = forms.CharField(widget=forms.Select(), required=False, label=_('province'))
    district = forms.CharField(widget=forms.Select(), required=False, label=_('district'))
    street = forms.CharField(required=False, label=_('street'))
    foreign_address = forms.CharField(label=_('address'), required=False)
    photo = forms.FileField(required=False, label=_('upload a photo'), widget=forms.TextInput(
        attrs={'class': 'sr-only inputFile', 'id': 'inputFile', 'accept': '.jpg,.jpeg,.png,.gif,.bmp,.tiff',
               'type': 'file'}, ))


    def __init__(self, data=None, initial=None, department=None, province=None, form_edit=None,
                 *args, **kwargs):
        """Init."""
        super(SellerForm, self).__init__(data=data, initial=initial, *args, **kwargs)
        departments = Department.objects.all()
        ciius = Ciiu.objects.all()
        countries = Countries.objects.all()

        if departments:
            self.fields['department'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in departments]

        if ciius:
            self.fields['ciiu'].widget.choices = [('', '')] + [(l.id, _(l.description)) for l in ciius]

        if countries:
            self.fields['nationality'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in countries]

        if countries:
            self.fields['residence_country'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in countries]


        if data and 'department' in data and data['department']:
            department = data['department']
        if data and 'province' in data and data['province']:
            province = data['province']

        if department:
            provinces = Province.objects.filter(department_id=department)
            self.fields['province'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in provinces]

        if province:
            districts = District.objects.filter(province_id=province)
            self.fields['district'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in districts]

        self.fields = Operations.setAdress(self, initial, self.fields)

    class Meta:
        """Meta de Vendedor."""

        model = Seller
        fields = ['nick', 'first_name', 'last_name', 'email_exact',
                  'telephone', 'cellphone', 'document_type', 'document_number',
                   'ruc' ]





class SellerFormFilters(FilterForm):
    """
    Filtrar el listado de vendedores
    """
    first_name = forms.CharField(required=False, label = _('first name'))
    last_name = forms.CharField(required=False, label = _('last name'))
    ruc = forms.CharField(required=False, label = _('RUC'))
    email_exact = forms.CharField(required=False, label = _('mail'))
    count_plans_seller = forms.IntegerField(required=False, label = _('number of plans sold greater than'))
    count_queries_seller = forms.IntegerField(required=False, label = _('number of queries sold greater than'))




class FromUntilFilters(FilterForm):
    """
    Filtrar por Fecha Picker
    """
    from_date = forms.DateField(required=False,
                                widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }), label = _('from'))
    until_date = forms.DateField(required=False,
                                widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }), label = _('until'))

"""
    Reportes de estado de cuenta
"""
class AccountStatusSellerFormFilters(FromUntilFilters):
    """
    Formulario para filtrar estados de cuenta por vendedor
    """
    seller = forms.CharField(widget=forms.Select(), required=True, label=_('seller'))
    show_sum_column = forms.BooleanField(label=_('Show Total'))

    def __init__(self,initial=None, token=None, *args, **kwargs):
        super(AccountStatusSellerFormFilters, self).__init__(initial, token, *args, **kwargs)
        obj_api = api()

        # Traer vendedores directamente desde la api
        # y actualizamos los options del select
        # "?page_size=0" trae un listado, ignorando la paginacion
        data = obj_api.get(slug='sellers/?page_size=0', token=token)

        if type(data) is list:
            self.fields['seller'].widget.choices = [('', '')] + [(l['id'], l['first_name']+' '+l['last_name']) for l in data]

"""
    Reporte de Autorizacion de clientes
"""
class AuthorizationClientFilter(FromUntilFilters):
    """
        Formulario para filtrar el listado de autorizacion de clientes
    """
    status = forms.CharField(widget=forms.Select(), label=_('status'))

    def __init__(self, *args, **kwargs):
        super(AuthorizationClientFilter, self).__init__(*args, **kwargs)

        status = Ch.user_status

        if type(status) is tuple:
            status = list(status)
            del status[3]  # Eliminamos el atributo desactivado
            status = tuple(status)
            self.fields['status'].widget.choices = [('', '')]
            self.fields['status'].widget.choices += status

"""
    Reporte de Pagos Pendientes
"""
class PendingPaymentFilter(FilterForm, ErrorsFieldsApi):
    """
        Formulario para filtrar el listado de pagos pendientes
    """
    document_number = forms.CharField(required=True, label = _('Document Client'))

    def __init__(self, *args, **kwargs):
        super(PendingPaymentFilter, self).__init__(*args, **kwargs)
