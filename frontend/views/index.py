
from django.shortcuts import render
from api.connection import api
from login.utils.tools import role_client_check, role_seller_check, role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class Client:
    @method_decorator(user_passes_test(role_client_check()))
    def index(self, request):
        """Inicio Cliente."""
        token = request.session['token']
        # import pdb; pdb.set_trace()
        obj_api = api()
        data_plans = obj_api.get(slug='clients/plans/', token=token, request=request)
        # print(data_plans)
        # form = ActivePlansForm()
        return render(request,
                          'frontend/actors/client/base_client.html')

class Seller:
    @method_decorator(user_passes_test(role_seller_check()))
    def index(self, request):
        return render(request, 'frontend/actors/seller/index.html')

class Specialist:
    @method_decorator(user_passes_test(role_specialist_check()))
    def index(self, request):
        return render(request, 'frontend/actors/specialist/base_specialist.html')
