"""Vista para Query."""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.connection import api


def upload_file(request):
        """Enviar data de archivos."""
        obj_api = api()
        files = request.FILES
        query = request.POST.get('query')

        token = request.session["token"]
        slug = 'queries/upload_files/{}'.format(query);

        resp = obj_api.put_all(slug=slug, token=token, files=files)
        
        if resp.status_code==200:
            return JsonResponse({})
        else:
            return JsonResponse({"error":resp.status_code})

