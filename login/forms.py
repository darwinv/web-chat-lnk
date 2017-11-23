from django import forms
from django.utils.translation import ugettext_lazy as _


class Login(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('User'), 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}))
