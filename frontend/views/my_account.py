
from django.http import JsonResponse
from django.shortcuts import render
from api.models import Ciiu
from api.connection import api

class Client:
    def account_profile(self, request, pk):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='clients/' + pk + "/", token=token)
        if resp["type_client"] == 'n':
            display_name = resp["first_name"] + ' ' + resp["last_name"]
        else:
            display_name = resp["agent_firstname"] + ' ' + resp["agent_lastname"]     

        try:
            ciiu = Ciiu.objects.get(pk=resp['ciiu'])
        except Ciiu.DoesNotExist:
            ciiu = None   

        return render(request, 'frontend/actors/client/my_account.html', {'data_user': resp, 'ciiu':ciiu, 'name':display_name})

class Specialist:
    def account_profile(self, request, pk):
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='specialists/' + pk + "/", token=token)
        name = resp["first_name"] + ' ' + resp["last_name"]
        if resp["type_specialist"] == 'm':
            type_specialist = 'Especialista Principal'
        else:
            type_specialist = 'Especialista Asociado'                
            
        
        if resp:
            return render(request, 'frontend/actors/specialist/my_account.html', {'data_user':resp, 'name':name,
                                                                                 'type_specialist': type_specialist})
        else:
            return JsonResponse({})
