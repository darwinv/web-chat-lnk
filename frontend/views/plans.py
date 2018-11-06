
import json
from django.http import JsonResponse
from api.connection import api
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

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
        resp = obj_api.get(slug='clients/plans-all/', token=token)
        if resp['count'] > 0:
            return render(request, 'frontend/actors/client/plan_list.html', {'plans': resp['results']})
        else:
            return JsonResponse({'message': _('You don\'t have active plans'),
                                 'class': 'successful'})

    def plan(self, request, pk):
        """ Plan efectivo """

        obj_api = api()
        token =  request.session['token']
        resp =  obj_api.get(slug='clients/plans/' + pk + '/', token=token)
        if resp:
            return render(request, 'frontend/actors/client/plan_detail.html', {'plan': resp})
        else:
            return JsonResponse({'message': _('That plan doesn\'t exist'),
                                 'class': 'successful'})

    def transfer(self, request, pk):
        return render(request, 'frontend/actors/client/plan_transfer.html')

    def empower(self, request, pk):
        pass

    def share(self, request, pk):
        pass

    def upload(self, request, pk):
        """ Subir voucher de Plan efectivo """

        obj_api = api()
        token =  request.session['token']
        resp =  obj_api.get(slug='clients/plans/' + pk + '/', token=token)
        if resp:
            return render(request, 'frontend/actors/client/plan_upload.html', {'plan': resp})
        else:
            return JsonResponse({'message': _('That plan doesn\'t exist'),
                                 'class': 'successful'})
