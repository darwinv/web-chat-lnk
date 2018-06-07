"""Vista para Query."""
import json
from django.shortcuts import render
from django.http import JsonResponse
from api.connection import api


def upload_file(request):
    """Vista para adjuntar archivo a una consulta"""
    print(request.POST)
    print(request.FILES)
    return JsonResponse(
        {'message': 'exito',
         'class': 'successful'})
