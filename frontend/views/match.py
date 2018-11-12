from django.shortcuts import render
from operator import itemgetter
from api.connection import api

class Client:
    def __init__(self):
        self.url_client = 'client/matchs/'

    def list_match(self, request):
        """Listado de Matchs."""
        obj_api = api()
        token = request.session['token']
        data_matchs = obj_api.get(slug=self.url_client, token=token)
        if data_matchs:
            match_list = sorted(data_matchs["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/client/match.html', {'match_list': match_list})