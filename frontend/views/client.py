"""Vista para el cliente."""
from django.shortcuts import render
from api.connection import api
from operator import itemgetter
from login.utils.tools import role_client_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from frontend.forms import QueryForm

class Client:
    @method_decorator(user_passes_test(role_client_check()))
    def index(self, request):
        return render(request, 'frontend/actors/client/base_client.html')

    @method_decorator(user_passes_test(role_client_check()))
    def chat(self, request, pk):
        """Chat por Especialidad."""
        obj_api = api()
        token = request.session['token']
        data_messages = obj_api.get(slug='queries/categories/' + pk,
                                    token=token)
        # Ordenamos el listado de mensajes para que los mas recientes salgan
        # abajo.
        form = QueryForm()
        newlist = sorted(data_messages["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/client/chat.html',
                      {'messages': newlist, 'form': form})
