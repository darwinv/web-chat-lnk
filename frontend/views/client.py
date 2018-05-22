"""Vista para el cliente."""
import json
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
        data_plans = obj_api.get(slug='clients/plans/', token=token, request=request)
        # print(data_plans)
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
        return JsonResponse(
            {'message': _('your plan has been chosen correctly'),
             'class': 'successful'})
    else:
        return JsonResponse({'message': _('there is an error'),
                             'class': 'error'})


def send_query(request):
    """Enviar data de consulta."""
    import pdb; pdb.set_trace()
    data = json.loads(request.POST.get('query_data'))
    obj_api = api()
    # import pdb; pdb.set_trace()
    token = request.session["token"]
    messages_list = [data['message_text']]
    query_payload = {
        "title": data["title"],
        "category": data["category"],
        "message": messages_list
    }

    resp = obj_api.post(slug='client/queries/', token=token, arg=query_payload)
    # data = json.loads(request.POST)
    print(resp)
    return JsonResponse({'message': 'llego'})

def activate_plan(request, code):
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


def get_plans_code(request, code):
    """Traer Planes sin activar por Pin."""
    obj_api = api()
    token = request.session['token']
    resp = obj_api.get(slug='activations/plans/' + code, token=token)
    return JsonResponse(resp)


def plans(request):
    """Planes Activos."""
    obj_api = api()
    token = request.session['token']
    resp = obj_api.get(slug='clients/plans/', token=token)
    if resp['count'] > 0:
        return JsonResponse(resp)
