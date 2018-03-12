"""Vista para el cliente."""
from django.shortcuts import render
from api.connection import api


class Client:

    def index(self, request):
        return render(request, 'frontend/actors/client/categories.html')

    def chat(self, request, pk):
        """Chat por Especialidad."""
        obj_api = api()
        token = request.session['token']
        # request.user.id
        data_messages = obj_api.get(slug='queries/categories/' + pk, token=token)
        # import pdb; pdb.set_trace()
        return render(request, 'frontend/chat.html', {'messages': data_messages["results"],
                                                      'user_id': request.user.id})
