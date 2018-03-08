"""Vista para el cliente."""
from django.shortcuts import render


class Client:

	def index(self, request):
		return render(request, 'frontend/actors/client/index.html')

    def chat(self, request):
		"""Chat por Especialidad."""
		pass
