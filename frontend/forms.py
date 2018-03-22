"""Formularios."""
from django import forms
from django.utils.translation import ugettext_lazy as _


class QueryForm(forms.Form):
    """Formulario de Consulta Cliente."""

    title = forms.CharField(label=_('title'), max_length=100)
    message = forms.CharField(label='')

    title.widget.attrs.update({'id': 'title_query', 'class': 'form-control',
                              'placeholder': 'Write your query'})

    message.widget.attrs.update({'id': 'text_message', 'class': 'form-control',
                                'placeholder': 'Send your Message'})
