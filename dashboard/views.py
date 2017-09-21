from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from api.connection import api
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext_lazy as _

from api.json2table import convert


#project
from mysite.settings import API_CLIENT_ID
from mysite.settings import API_CLIENT_SECRET
from mysite.settings import API_URL

class Specialist:

    def showSpecialistProfile(request,client_id):        
        ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})

@login_required()
def showList(request):
    ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
    json_object = ObjApi.get('clients/')

    # json_object = {"key" : "value","key2" : "value2","key3" : "value3","key4" : "value4"}

    customColumn = {"last_name": {'username', 'last_name'}}

    header = {"Lastname": "last_name", "Code": "code", "Email": "email_exact", "RUC": "ruc", "Category": "institute",
              "Specialty": "nationality"}
    table_attributes = {"class": "table table-striped table-bordered table-hover"}

    #data = convert(json_object, table_attributes=table_attributes, header=header, customColumn=customColumn)

    #return render(request, 'admin/actor/specialistList.html', {'data': data})
    return render(request, 'admin/actor/specialistList.html')

class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):        
        ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})