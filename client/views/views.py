from django.shortcuts import render


def tempPage(request):
	return render(request, 'client/tempPage.html')