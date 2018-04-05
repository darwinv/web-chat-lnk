"""Vista Especialista."""

from django.shortcuts import render
from operator import itemgetter
from login.utils.tools import role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from api.connection import api
from frontend.forms import QueryForm

class Specialist:
    @method_decorator(user_passes_test(role_specialist_check()))
    def index(self, request):
        return render(request, 'frontend/actors/specialist/base_specialist.html')

    @method_decorator(user_passes_test(role_specialist_check()))
    def chat(self, request, pk):
        """Chat por Cliente."""
        obj_api = api()
        token = request.session['token']
        messages = None

        data_messages = obj_api.get(slug='queries/clients/' + pk, token=token)
        import pdb
        pdb.set_trace()
        # Ordenamos el listado de mensajes
        # para que los mas recientes salgan abajo.
        form = QueryForm()
        if data_messages:
            messages = sorted(data_messages["results"], key=itemgetter('id'))
        return render(request, 'frontend/actors/specialist/chat.html',
                      {'messages': messages, 'form': form})
