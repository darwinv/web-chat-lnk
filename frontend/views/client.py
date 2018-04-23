"""Vista para el cliente."""
from django.shortcuts import render
from django.http import JsonResponse
from api.connection import api
from operator import itemgetter
from login.utils.tools import role_client_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from frontend.forms import QueryForm, ActivePlansForm
from api.models import Category
from django.utils.translation import ugettext_lazy as _


class Client:
    """Vista del Cliente."""

    @method_decorator(user_passes_test(role_client_check()))
    def index(self, request):
        """Inicio Cliente."""
        token = request.session['token']
        # import pdb; pdb.set_trace()
        obj_api = api()
        data_plans = obj_api.get(slug='clients/plans/', token=token,
                                 request=request)
        print(data_plans)
        # form = ActivePlansForm()
        return render(request,
                      'frontend/actors/client/base_client.html')

    @method_decorator(user_passes_test(role_client_check()))
    def chat(self, request, pk):
        """Chat por Especialidad."""
        obj_api = api()
        token = request.session['token']

        messages = None
        data_messages = obj_api.get(slug='queries/categories/' + pk,
                                    token=token)
        # Ordenamos el listado de mensajes para que los mas recientes salgan
        # abajo.
        esp = Category.objects.get(pk=pk)
        form = QueryForm()
        if data_messages:
            messages = sorted(data_messages["results"], key=itemgetter('id'))

        return render(request, 'frontend/actors/client/chat.html',
                      {'messages': messages, 'form': form, 'speciality': esp})


def set_chosen_plan(request, pk):
    """Elegir plan para consultar."""
    obj_api = api()
    token = request.session['token']
    resp = obj_api.put(slug='chosens-plans/' + pk, token=token,
                       arg=request.POST)
    if 'id' in resp:
        return JsonResponse({'message': _('your plan has been chosen correctly'),
                             'class': 'successful'})
    else:
        return JsonResponse({'message': _('there is an error'),
                             'class': 'error'})


def plans(request):
    """Planes Activos."""
    obj_api = api()
    token = request.session['token']
    resp = obj_api.get(slug='clients/plans/', token=token)
    if resp['count'] > 0:
        return JsonResponse(resp)
