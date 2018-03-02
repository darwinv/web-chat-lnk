from django.shortcuts import render

class Client:

	def tempPage(self, request):
		return render(request, 'frontend/tempPage.html')