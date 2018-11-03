
import json
from django.http import JsonResponse
from api.connection import api
from django.utils.translation import ugettext_lazy as _

class Client:
    def set_chosen_plan(self, request, pk):
        """Elegir plan para consultar."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.put(slug='chosens-plans/' + pk, token=token,
                           arg=request.POST)
        if 'id' in resp:
            return JsonResponse(
                {'message': _('your plan has been chosen correctly'),
                 'class': 'successful'})
        else:
            return JsonResponse({'message': _('there is an error'),
                                 'class': 'error'})

    def activate_plan(self, request, code):
        """Activar Plan por codigo PIN."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.put(slug='activations/plans/' + code, token=token)
        if 'id' in resp:
            return JsonResponse(
                {'message': _('your plan has been activated'),
                 'class': 'successful'})
        else:
            return JsonResponse({'message': _('there is an error'),
                                 'class': 'error'})
        return JsonResponse(resp)


    def get_plans_code(self, request, code):
        """Traer Planes sin activar por Pin."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='activations/plans/' + code, token=token)
        return JsonResponse(resp)


    def plans(self, request):
        """Planes Activos."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='clients/plans/', token=token)
        if resp['count'] > 0:
            return JsonResponse(resp)

     def get_status_footer(self, request):
         """Status del footer."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='plans/check_status/', token=token)
        return JsonResponse(resp)       
