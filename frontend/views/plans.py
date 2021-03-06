
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
        
        if resp and 'id' in resp:
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

        if 'results' in resp:
            plans = resp['results']
        else:
            plans = None

        if 'count' in resp:
            count = resp['count']
        else:
            count = None


        return render(request, 'frontend/actors/client/plan_list.html', {'plans': plans, 'count':count})

    def plan(self, request, pk):
        """ Plan efectivo """

        obj_api = api()
        token =  request.session['token']
        plan =  obj_api.get(slug='clients/plans/' + pk + '/', token=token)
        status = plan['status']
        fee = plan['fee']
        fee_order_number = fee['fee_order_number'] if fee else 0
        validating = fee and fee['status'] == 3

        clickable = status == 1 or plan['is_fee'] and fee and fee['status'] == 1 or status == 3
        clients = obj_api.get(slug='clients/plans-share-empower/' + pk + '/', token=token)

        if 'results' in clients:
            clients = clients['results']
        else:
            clients = None
        return render(request, 'frontend/actors/client/plan_detail.html', {
            'plan': plan, 'clients':clients, 'clickable':clickable,
            'fee_order_number':fee_order_number, 'validating':validating
        })


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

    def summary(self, request, sale_id):
        """ Resumen de Plan efectivo """

        obj_api = api()
        token =  request.session['token']
        resp =  obj_api.get(slug='clients/sales/detail/' + sale_id + '/', token=token)
        
        fee = resp['fee']

        if fee:
            total = float(fee['fee_amount'])
            fee_order_number = fee['fee_order_number']
        else:
            total = 0
            fee_order_number = 0

        products_api = resp['products']

        products = []
        for product in products_api:
            plan = product['plan']
                
            plan_name = plan['plan_name']
            payed = plan['queries_to_pay'] == 0
            total_queries = plan['query_quantity']
            price = float(product['price'])
            validity = plan['validity_months']
            if resp['is_fee']:
                fee_queries = total_queries // validity
                price /= validity
            else:
                fee_queries = None

            products.append({'name':plan_name, 'total_queries':total_queries, 'fee_queries':fee_queries, 
                             'validity':validity, 'price':price, 'payed':payed})

        sale_id = resp['id']

        if not fee or fee['status'] != 1:
            validating = fee and fee['status'] == 3
            return render(request, 'frontend/actors/client/summary.html', {
                'products':products, 'total':total, 'validating':validating, 'fee_order_number':fee_order_number
            })
        return render(request, 'frontend/actors/client/summary.html', {
            'products':products, 'total':total, 'pk':sale_id
        })


    def get_status_footer(self, request):
        """Status del footer."""
        obj_api = api()
        token = request.session['token']
        resp = obj_api.get(slug='plans/check_status/', token=token)
        return JsonResponse(resp)       
