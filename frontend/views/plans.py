
import json
from django.http import JsonResponse
from api.connection import api
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from frontend.forms import EmailCheckForm, PlanActionForm

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
        plan =  obj_api.get(slug='clients/plans/' + pk + '/', token=token)
        clients = obj_api.get(slug='clients/plans-share-empower/' + pk + '/', token=token)

        if plan and clients and 'results' in clients:
            return render(request, 'frontend/actors/client/plan_detail.html', {'plan': plan, 'clients':clients['results']})
        else:
            return JsonResponse({'message': _('That plan doesn\'t exist'),
                                 'class': 'successful'})

    def action(self, request, pk, action):
        email_check_form = EmailCheckForm()
        plan_action_form = PlanActionForm()
        acquired_plan = pk
        type_operation = ['transfer', 'empower', 'share'].index(action) + 1

        obj_api = api()
        token =  request.session['token']
        resp =  obj_api.get(slug='clients/plans/' + pk + '/', token=token)
        available_queries = resp['available_queries']

        return render(request, 'frontend/actors/client/plan_action.html', {
            'action':action, 'email_check_form':email_check_form, 'plan_action_form':plan_action_form,
            'acquired_plan':acquired_plan, 'type_operation':type_operation, 'available_queries':available_queries
        })

    def summary(self, request, pk):
        """ Resumen de Plan efectivo """

        obj_api = api()
        token =  request.session['token']
        data = {'client':request.user.id}
        resp =  obj_api.get(slug='clients/sales/have-payment-pending/', arg=data, token=token)

        product = resp['products'][0]

        total = product['price']
        plan = product['plan']
        lines = [
            plan['plan_name'],
            str(plan['query_quantity']) + " queries",
            "Validty " + str(plan['validity_months']) + " months",
            "S/. " + str(total)
        ]

        sale_id = product['sale']

        if resp and lines:
            return render(request, 'frontend/actors/client/summary.html', {'lines': lines, 'total': total, 'pk':sale_id})
        else:
            return JsonResponse({'message': _('That plan doesn\'t exist'),
                                 'class': 'successful'})

    def get_status_footer(self, request):
        """Status del footer."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='plans/check_status/', token=token)
        return JsonResponse(resp)       
