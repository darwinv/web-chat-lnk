
import json
from django.shortcuts import render
from django.http import JsonResponse
from api.connection import api
from operator import itemgetter
from login.utils.tools import role_client_check, role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from frontend.forms import QueryForm
from api.models import Category

class Client:

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

    def send_query(self, request):
        """Enviar data de consulta."""
        obj_api = api()
        data = json.loads(request.POST.get('query_data'))
        token = request.session["token"]
        resp = None

        if "msg_type" in data["message"][0]:
            if "query" in data:
                query = data["query"]

            if data["message"][0]["msg_type"]=="q":
                resp = obj_api.post_all(slug='client/queries/', token=token, arg=data)
            if data["message"][0]["msg_type"]=="a":
                resp = obj_api.put_all(slug='specialist/queries/{}/'.format(query), token=token, arg=data)
            if data["message"][0]["msg_type"]=="r":
                resp = obj_api.put_all(slug='client/queries/{}/'.format(query), token=token, arg=data)

            if resp:
                return JsonResponse(resp.json())
        
        return JsonResponse({"msg_type":"required"})

class Specialist:

    @method_decorator(user_passes_test(role_specialist_check()))
    def chat(self, request, pk):
        """Chat por Cliente."""
        obj_api = api()
        token = request.session['token']
        messages = None

        data_messages = obj_api.get(slug='queries/clients/' + pk, token=token)
        # Ordenamos el listado de mensajes
        # para que los mas recientes salgan abajo.
        form = QueryForm()
        if data_messages:
            messages = sorted(data_messages["results"], key=itemgetter('id'))

        return render(request, 'frontend/actors/specialist/chat.html',
                      {'messages': messages, 'form': form})