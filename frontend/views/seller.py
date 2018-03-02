from django.shortcuts import render

class Seller:
	def tempPage(request):
		return render(request, 'frontend/tempPage.html')