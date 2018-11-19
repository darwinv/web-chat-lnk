"""Formularios."""
from django import forms
from django.utils.translation import ugettext as _
from api.models import Category


class QueryForm(forms.Form):
    """Formulario de Consulta Cliente."""

    title = forms.CharField(label=_('title'), max_length=100)
    message = forms.CharField(label='')
    title.widget.attrs.update({'id': 'title', 'class': 'form-control',
                              'placeholder': 'Write your query'})

    message.widget.attrs.update({'id': 'text_message', 'class': 'form-control',
                                'placeholder': 'Send your Message'})


class ActivePlansForm(forms.Form):
    """Formulario para listar y actualizar el plan elegido."""

    active_plans = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, plans, *args, **kwargs):
        """Init."""
        super(ActivePlansForm, self).__init__(*args, **kwargs)
        newplans = format_choices(plans)
        self.fields['active_plans'].choices = [(l['id'], l['value'])
                                               for l in newplans]

class ContactForm(forms.Form):
    """Formulario de contacto(Soporte)"""

    title = forms.CharField(label='', max_length=100)
    message = forms.CharField(label='')
    message.widget = forms.Textarea()
    title.widget.attrs.update({'id': 'title_contact', 'class': 'form-control contact-field',
                              'placeholder': _('Title of your concern')})

    message.widget.attrs.update({'id': 'text_message', 'class': 'form-control contact-field',
                                'placeholder': _('Write what you want to tell us')})

def format_choices(plans):
    """Formato para opciones."""
    newplan = plans.copy()
    for l in range(0, len(plans)):
        # del newplan[l]['available_queries']
        # del newplan[l]['query_quantity']
        # import pdb; pdb.set_trace()
        newplan[l]['id'] = plans[l]['id']
        newplan[l]['value'] = plans[l]['plan_name'] + ' | ' +\
            _('availables') + ': ' + str(plans[l]['available_queries']) +\
            '/' + str(plans[l]['query_quantity']) + ' | ' +\
            _('expiration date') + ': ' + plans[l]['expiration_date']
    return newplan

class EmailCheckForm(forms.Form):

    email = forms.EmailField(max_length=150, required=True)
    email.widget.attrs.update({'id': 'email-box', 'type':'email',
                               'placeholder': 'Email'})


class PlanActionForm(forms.Form):
    legal = forms.BooleanField(required=True)
    legal.widget.attrs.update({'id': 'legal-checkbox'})


class MatchForm(forms.Form):
    """Form para crear match."""
    category = forms.CharField(widget=forms.Select(), required=False, label='Seleccione la especialidad')
    subject = forms.CharField(label='Describe Tu Caso')
    subject.widget = forms.Textarea()
    category.widget.attrs['required'] = 'required'
    subject.widget.attrs.update({'id': 'subject', 'class': 'form-control',
                                 'placeholder': _('Write your query')})

    def __init__(self, data=None, initial=None, *args, **kwargs):
        super(MatchForm, self).__init__(data=data, initial=initial, *args, **kwargs)
        categories = Category.objects.all()
        if categories:
            self.fields['category'].widget.choices = [('', '')] + [(l.id, _(l.name)) for l in categories]
