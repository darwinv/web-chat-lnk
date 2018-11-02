
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

    def send_query(request):
        """Enviar data de consulta."""
        data = json.loads(request.POST.get('query_data'))
        files = json.loads(request.POST.get('files'))
        messages_list = [data['message_text']]
        message_file = {
            "message": "",
            "msg_type": "q"
            }

        for n_file in files:
            message_file.update({"content_type": 2, "file_url": n_file["name"]})
            messages_list.append(message_file)

        obj_api = api()

        token = request.session["token"]
        query_payload = {
            "title": data["title"],
            "category": data["category"],
            "message": messages_list
        }
        resp = obj_api.post(slug='client/queries/', token=token, arg=query_payload)
        # data = json.loads(request.POST)
        print(resp)
        return JsonResponse(resp)


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