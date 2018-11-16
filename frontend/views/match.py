from django.shortcuts import render
from operator import itemgetter
from api.connection import api
from login.utils.tools import role_client_check, role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
# from django.urls import reverse

class Client:
    def __init__(self):
        self.url_client_list = 'client/matchs/'
        self.url_client_detail = 'match/'

    @method_decorator(user_passes_test(role_client_check()))
    def list_match(self, request):
        """Listado de Matchs."""
        obj_api = api()
        token = request.session['token']
        data_matchs = obj_api.get(slug=self.url_client_list, token=token)
        if data_matchs:
            match_list = sorted(data_matchs["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/client/match_list.html', {'match_list': match_list})

    @method_decorator(user_passes_test(role_client_check()))
    def detail_match(self, request, pk):
        """Detalle de Match."""
        obj_api = api()
        token = request.session['token']
        data_match = obj_api.get(slug=self.url_client_detail + pk +"/", token=token)
        return render(request, 'frontend/actors/client/match_detail.html', {'match': data_match})       


class Specialist:
    def __init__(self):
        self.url_specialist_list = 'specialists/matchs/'
        self.url_specialist_detail = ''
        # self.decline_match = 'frontend:match-specialist-decline'

    @method_decorator(user_passes_test(role_specialist_check()))    
    def list_match(self, request):
        """Listado de Matchs."""
        obj_api = api()
        token = request.session['token']
        data_matchs = obj_api.get(slug=self.url_specialist_list, token=token)
        if data_matchs:
            match_list = sorted(data_matchs["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/specialist/match_list.html', {'match_list': match_list})

    # @method_decorator(user_passes_test(role_specialist_check()))   
    # def decline_match(self, request):
    #     """Vista para declinar Match."""    
    #     obj_api = api()
    #     token = request.session["token"]

    #     if request.method == 'POST':
           

