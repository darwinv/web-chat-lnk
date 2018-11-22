from login.utils.tools import role_client_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from api.connection import api
import json  

class Client:

    @method_decorator(user_passes_test(role_client_check()))
    def list_purchase(self, request):
        """Listado de productos."""
        return render(request, 'frontend/actors/client/purchase_list.html')

    @method_decorator(user_passes_test(role_client_check()))
    def list_purchase_plans(self, request):
        """Listado de planes."""
        obj_api = api()
        token = request.session['token']

        plans = obj_api.get(slug='plans/', token=token)
        return render(request, 'frontend/actors/client/purchase_plan_list.html',
                        {"plans":plans})


    @method_decorator(user_passes_test(role_client_check()))
    def summary_purchase_plans(self, request):
        """Resumen compra de planes."""
        obj_api = api()
        token = request.session['token']
        plans_purchase = []
        products = []
        ids_purchase = []
        plans = obj_api.get(slug='plans/', token=token)
        ids_plans = request.POST.getlist('vehicle')
        total = request.POST["total"]
        is_fee = int(request.POST["modality"])

        for i in range(0, len(ids_plans)): 
            id_p = int(ids_plans[i]) - 1
            plans_purchase.append(plans[id_p])
        

        for plan in plans_purchase:  
            id_plan = plan["id"]      
            plan_name = plan['name']
            ids_purchase.append(id_plan)
            total_queries = plan['query_quantity']
            price = float(plan['price'])
            validity = plan['validity_months']
            if is_fee==1:
                fee_queries = total_queries // validity
                price /= validity
            else:
                fee_queries = None

            products.append({'id':id_plan, 'name':plan_name, 'total_queries':total_queries,
                            'fee_queries':fee_queries, 'validity':validity, 'price':price})     
        # json_ids = json.loads(ids_purchase)
        return render(request, 'frontend/actors/client/summary_plans.html',
                        {"products":products, "total":total, "isfee":is_fee, "ids_plans":ids_purchase} )                
