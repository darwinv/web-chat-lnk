from django.shortcuts import render

class Seller:
	
	def index(self, request):
		return render(request, 'frontend/actors/seller/index.html')