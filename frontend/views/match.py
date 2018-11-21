from django.shortcuts import render
from operator import itemgetter
from api.connection import api
from login.utils.tools import role_client_check, role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from frontend.forms import MatchForm
from dashboard.tools import ToolsBackend
from django.http import JsonResponse

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

    @method_decorator(user_passes_test(role_client_check()))
    def create_match(self, request):
        """Crear Match."""
        form = MatchForm()
        return render(request, 'frontend/actors/client/match.html',
                      {'form': form})



class Specialist:
    def __init__(self):
        self.url_specialist_list = 'specialists/matchs/'
        self.url_specialist_detail = 'match/'

    @method_decorator(user_passes_test(role_specialist_check()))
    def list_match(self, request):
        """Listado de Matchs."""
        obj_api = api()
        token = request.session['token']
        data_matchs = obj_api.get(slug=self.url_specialist_list, token=token)
        if data_matchs:
            match_list = sorted(data_matchs["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/specialist/match_list.html', {'match_list': match_list})

    @method_decorator(user_passes_test(role_specialist_check()))
    def detail_match(self, request, pk):
        """Detalle de Match."""
        obj_api = api()
        token = request.session['token']
        data_match = obj_api.get(slug=self.url_specialist_detail + pk +"/", token=token)
        return render(request, 'frontend/actors/specialist/match_detail.html', {'match': data_match})

    @method_decorator(user_passes_test(role_specialist_check()))
    def summary(self, request, pk):
        """ Resumen de Match."""

        obj_api = api()
        token =  request.session['token']
        tool = ToolsBackend()


        resp =  obj_api.get(slug='match/'+ pk + '/', token=token)
        date = tool.datetime_format_to_view(resp['date'])

        photo = resp['category_image']
        id_match = resp['id']
        total = resp["price"]

        lines = [
            resp['category'],
            "Solicitado el: "+date,
            "S/. " + str(resp['price'])
        ]
        products = []
        products.append({'photo':photo, 'lines':lines})

        # sale_id = product['sale']

        if resp and lines:
            return render(request, 'frontend/actors/specialist/summary.html', {'products': products,
                                                                               'total': total, 'pk':id_match})
        else:
            return JsonResponse({'message': _('That match doesn\'t exist'),
                                 'class': 'error'})