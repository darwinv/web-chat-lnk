from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


from api.connection import api

from dashboard.json2table import convert,getActualPage
from dashboard.forms import SpecialistForm
import json
import pdb

class Account:
    logo_content_header    = "fa fa-calculator"
    title_content_header   = "{} - ".format(_("actors").title())

    def generateHeader(self,custom_title=None):
        if custom_title:
            title = self.title_content_header + custom_title
        else:
            title = self.title_content_header

        header = {'icon':self.logo_content_header,'title':title}
        return {**header, **self.vars_page}

class Specialist(Account):

    @method_decorator(login_required)
    def list(self,request,specialist_id):
        api = api()

        # Traer data para el listado
        data = api.get(slug='account_status/specialists/'+specialist_id,token=request.session['token'])

        vars_page  = self.generateHeader(custom_title=title_page)