
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
        resp = obj_api.post_all(slug='client/queries/', token=token, arg=data)
        return JsonResponse(resp.json())

    # def send_files(self, request):
    #     """Enviar data de archivos."""
    #     obj_api = api()
    #     files = json.loads(request.POST.get('files'))
    #     query = json.loads(request.POST.get('query'))
    #     token = request.session["token"]
    #     slug = 'queries/upload_files/{}/'.format(query);
    #     data = {
    #             'file': files
    #         }
        
    #     resp = obj_api.post(slug=slug, token=token, arg=data)
        
    #     return JsonResponse(resp)


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