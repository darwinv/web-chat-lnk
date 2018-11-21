from login.utils.tools import role_client_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from api.connection import api

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
                        {"plans":plans}