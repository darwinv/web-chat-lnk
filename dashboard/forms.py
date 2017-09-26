from django import forms
from django.utils.translation import ugettext_lazy as _

class createUser(forms.Form):
    nick                = forms.CharField(max_length=45, blank=True)
    email_exact         = forms.CharField(max_length=150, unique=True)
    telephone           = forms.CharField(max_length=14)
    cellphone           = forms.CharField(max_length=14)
    photo               = forms.CharField(max_length=250, default='preview.png') ## instalar pillow para ImageField
    options_documents   = (
                                ('0', 'DNI'),
                                ('1', 'Passport'),
                                ('2', 'Foreign Card'),
                            )
    document_type       = forms.CharField(max_length=1, choices=options_documents)
    document_number     = forms.CharField(max_length=45, unique=True)
    ruc                 = forms.CharField(max_length=40, unique=True, null=True)
    code                = forms.CharField(max_length=45, unique=True)
    anonymous           = forms.BooleanField(default=True)
    updated_at          = forms.DateTimeField(auto_now_add=True)
    nationality         = forms.ForeignKey(Countries, on_delete=forms.PROTECT, default=1)
    role                = forms.ForeignKey(Role, on_delete=forms.PROTECT, default=1)
    address             = forms.ForeignKey(Address, on_delete=forms.PROTECT, null=True)

class CreateForm(createUser):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name', 'summary', 'description']
        
class createSpecialist(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('user').title(), 'class': 'form-control'}) )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('password').title(), 'class': 'form-control'}) )
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('repeat password').title(), 'class': 'form-control'}) )
