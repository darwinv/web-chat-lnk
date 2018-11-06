"""Vista para Query."""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.connection import api


@csrf_exempt
def upload_file(request):
    """Vista para adjuntar archivo a una consulta"""
    print(request.POST)
    print(request.FILES)
    obj_api = api()
    token = request.session['token']
    pk = ""
    resp = obj_api.put(slug='queries/upload_files/' + pk, token=token)
    return JsonResponse(
        {'message': 'exito',
         'class': 'successful'})
