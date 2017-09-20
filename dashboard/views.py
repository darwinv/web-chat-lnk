from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from api.connection import api
from django.contrib.auth.decorators import login_required

class Specialist:

    def showSpecialistProfile(request,client_id):        
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})

@login_required()
def showList(request):
    return render(request, 'admin/actor/specialistList.html')

class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):        
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})