from django import forms
from django.utils.translation import ugettext_lazy as _
from api.api_choices_models import ChoicesAPI as Ch
from api.models import Client, Department, Countries, Ciiu, LevelInstruction, EconomicSector, Province, District
from django.forms import ModelForm
from dashboard.forms import ErrorsFieldsApi as ErrorField


class Login(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('User'), 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}))

class RegisterClientForm(forms.Form):
    select_search = {'data-live-search':'true','class':'selectpicker'}
    # Campos Generales para Cliente
    type_client = forms.ChoiceField(choices=Ch.client_full_type_client, widget=forms.RadioSelect(attrs={'class': 'radio-input radio-type-client'}))    
    document_type = forms.ChoiceField(choices=Ch.user_document_type, widget=forms.RadioSelect(attrs={'class': 'radio-input'}))
    nick = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Nick')}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Repeat Password')}))
    document_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Identification document')}))
    residence_country = forms.CharField(widget=forms.Select(), label=_('residence country'))
    nationality = forms.CharField(widget=forms.Select(), label=_('nationality'))
    department = forms.CharField(widget=forms.Select(), required=False)
    province = forms.CharField(widget=forms.Select(), required=False)
    district = forms.CharField(widget=forms.Select(), required=False)
    street = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Address')}))
    foreign_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Address')}))
    email_exact = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Email')}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Telephone')}), required=False)
    cellphone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Cellphone')}), required=False)
    photo = forms.FileField(required=False, label=_('upload a photo'), widget=forms.TextInput(
        attrs={'class': 'sr-only inputFile', 'id': 'inputFile', 'accept': '.jpg,.jpeg,.png,.gif,.bmp,.tiff', 'type': 'file'}, ))
    activity_description = forms.CharField(label=_('Describe your activity'), widget=forms.Textarea(), required=False)
    about = forms.CharField(label=_('Tell us what you do to know more about yourself.'), widget=forms.Textarea(), required=False)

    def __init__(self, data=None, *args, **kwargs):
        """Init."""
        super(RegisterClientForm, self).__init__(data=data, *args, **kwargs)
        departments = Department.objects.all()
        countries = Countries.objects.all()
        department = province = None

        if departments:
            self.fields['department'].widget.choices = [('', _('Department'))] + [(l.id, _(l.name)) for l in
                                                                                  departments]
            self.fields['province'].widget.choices = [('', _('Province'))]
            self.fields['district'].widget.choices = [('', _('District'))]

        if data and 'department' in data and data['department']:
            department = data['department']
            
        if data and 'province' in data and data['province']:
            province = data['province']
            
        if department:
            provinces = Province.objects.filter(department_id=department)
            self.fields['province'].widget.choices = [('', _('Province'))] + [(l.id, _(l.name)) for l in provinces]

        if province:
            districts = District.objects.filter(province_id=province)
            self.fields['district'].widget.choices = [('', _('District'))] + [(l.id, _(l.name)) for l in districts]

        if countries:
            self.fields['residence_country'].widget.choices = [('', _('Country'))] + [(l.id, _(l.name)) for l in countries]
            self.fields['nationality'].widget.choices = [('', _('Country'))] + [(l.id, _(l.name)) for l in countries]

    def clean(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')

        if password and password != repassword:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class RegisterClientFormNatural(RegisterClientForm, ErrorField):

    # Campos para Cliente Natural
    sex = forms.ChoiceField(choices=Ch.client_sex, widget=forms.RadioSelect(attrs={'class': 'radio-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Last name')}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('First name')}))
    civil_state = forms.CharField(widget=forms.Select(attrs={'class':'cap'}), label=_('civil state'))
    birthdate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}), label = _('birthdate'))
    level_instruction = forms.CharField(widget=forms.Select(), label=_('Degree of instruction'))
    institute = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Institute')}), required=False)
    profession = forms.CharField(label=_('Profession'))
    ocupation = forms.CharField(widget=forms.Select(), label=_('Ocupation'))
    ciiu = forms.CharField(widget=forms.Select(), required=False)

    def __init__(self, data=None, *args, **kwargs):
        """Init."""
        super(RegisterClientFormNatural, self).__init__(data=data, *args, **kwargs)

        level_instructions = LevelInstruction.objects.all()
        ciius = Ciiu.objects.all()
        
        if ciius:
            self.fields['ciiu'].widget.choices = [('', _('CIIU'))] + [(l.id, _(l.description)) for l in ciius]

        if level_instructions:
            self.fields['level_instruction'].widget.choices = [('', _('Level instruction'))] + [(l.id, _(l.name))
                                                                                     for l in level_instructions]
        if type(Ch.client_civil_state) is tuple:
            self.fields['civil_state'].widget.choices += (('', '')),
            self.fields['civil_state'].widget.choices += Ch.client_civil_state

        if type(Ch.client_ocupation) is tuple:
            self.fields['ocupation'].widget.choices += (('', '')),
            self.fields['ocupation'].widget.choices += Ch.client_ocupation


class RegisterClientFormBusiness(RegisterClientForm, ErrorField):
    
    # Campos para Cliente Juridico
    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('business name')}))
    commercial_reason = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('commercial reason')}))
    ruc = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    agent_firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('agent firstname')}))
    agent_lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('agent lastname')}))
    position = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Position in the company')}))
    economic_sector = forms.CharField(widget=forms.Select())
    ciiu = forms.CharField(widget=forms.Select())

    def __init__(self, data=None, *args, **kwargs):
        """Init."""
        super(RegisterClientFormBusiness, self).__init__(data=data, *args, **kwargs)

        economic_sectors = EconomicSector.objects.all()
        ciius = Ciiu.objects.all()

        if economic_sectors:
            self.fields['economic_sector'].widget.choices = [('', _('economic sector'))] + [(l.id, _(l.name)) for l in
                                                                                  economic_sectors]
        if ciius:
            self.fields['ciiu'].widget.choices = [('', _('CIIU'))] + [(l.id, _(l.description)) for l in ciius]
