
from django.shortcuts import render

class Client:

    @method_decorator(user_passes_test(role_client_check()))
    def list_purchase(self, request):
        """Listado de productos."""
        return render(request, 'frontend/actors/client/purchase_list.html')

    @method_decorator(user_passes_test(role_client_check()))
    def list_purchase_plans(self, request):
        """Listado de planes."""
        pass