from django.shortcuts import render

class Specialist:
	
	def index(self, request):
		return render(request, 'frontend/actors/specialist/index.html')