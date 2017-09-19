from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from api.connection import api

class Specialist:

    def showList(request):
        return render(request, 'admin/actor/specialistList.html')

    def showSpecialistProfile(request,client_id):        
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})


class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):        
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})