from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views import View

import requests
import logging

class api:
    _url = 'http://localhost:3000/'
    def __init__(self):
        pass

    def get(self,arg):
        try:
            #r = requests.get(self._url+arg)
            r = requests.get('http://localhost:3001/users/')              
            return r.json()
        except Exception as e:
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)

            
class Client:

    def showList(request):
        return render(request, 'admin/index.html')

    def showClientProfile(request,client_id):        
        ObjApi = api()
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})