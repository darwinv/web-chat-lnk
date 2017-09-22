from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from api.connection import api
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _

from api.json2table import convert



class Specialist:

    def showSpecialistProfile(request,client_id):
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})

#@login_required()
def showList(request):
    # print(request.user.is_authenticated())
    # print("--------------------------------")
    ObjApi = api()
    json_object = ObjApi.get('specialist/')


    customColumn = {"last_name": {'username', 'last_name'}}

    header = {"Lastname": "last_name", "Code": "code", "Email": "email_exact", "RUC": "ruc", "Category": "institute",
              "Specialty": "nationality"}
    
    tablaSpecialist = convert(json_object, header=header, customColumn=customColumn)

    return render(request, 'admin/actor/specialistList.html', {'tablaSpecialist': tablaSpecialist})
    
class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):        
        ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})