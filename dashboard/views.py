from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from api.connection import api
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _

from dashboard.json2table import convert
from dashboard.json2table import getActualPage





class Specialist:

    def showSpecialistProfile(request,client_id):
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})

@login_required()
def showList(request):

    actualPage  = getActualPage(request)

    arg         = {"page": actualPage}
    ObjApi      = api()
    data        = ObjApi.get(slug='specialist/',arg=arg,request=request)


    customColumn    = {"last_name": {'type':'concat','data':{'username', 'last_name'}},
                       "detail": {'type':'detail','data':{'href':'dashboard:actor-specialists-edit','key':'id'}}
                    }
    lastnamesTittle = "{} {} {}".format(_("surnames"),_("and"),_("names"))
    header          = {lastnamesTittle: "last_name", _("code"): "code", _("email"): "email_exact", _("RUC"): "ruc", _("category"): "institute",
                       _("specialty"): "nationality",_("detail"): "detail"}
    tablaSpecialist = convert(data, header=header,actualPage=actualPage, customColumn=customColumn )


    return render(request, 'admin/actor/specialistList.html', {'tablaSpecialist': tablaSpecialist})
    

class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):
        ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})