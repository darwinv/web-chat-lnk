


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