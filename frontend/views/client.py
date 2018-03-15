"""Vista para el cliente."""
from django.shortcuts import render
from api.connection import api
from operator import itemgetter

class Client:

    def index(self, request):
        return render(request, 'frontend/actors/client/categories.html')

    def chat(self, request, pk):
        """Chat por Especialidad."""
        obj_api = api()
        token = request.session['token']
        data_messages = obj_api.get(slug='queries/categories/' + pk, token=token)
        # Ordenamos el listado de mensajes para que los mas recientes salgan abajo.
        # import pdb; pdb.set_trace()
        newlist = sorted(data_messages["results"], key=itemgetter('id'))
        return render(request, 'frontend/chat.html', {'messages': newlist,
                                                      'user_id': request.user.id,
                                                      'token_user': token})
