from django.shortcuts import render

class Specialist:
	def tempPage(request):
		return render(request, 'frontend/tempPage.html')