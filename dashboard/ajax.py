from api.connection import api
from django.http import JsonResponse
from django.http import QueryDict
import json

def ajax_service(request):
    """Planes Activos."""
    obj_api = api()
    if request.method == 'PUT':
        data = QueryDict(request.body)
    else:
        data = getattr(request, request.method)

    if request.FILES:
        files = request.FILES
    else:
        files = None
    if 'use_method' in data:
        request.method = data['use_method']

    if 'url' in data:
        url = data['url']
    else:
        return JsonResponse()

    if 'token' in request.session:
        token = request.session['token']
    else:
        token = None
    
    data = clean_data_files(request, data)

    if 'serialize' in data:
        data = serialize_keystr_to_json(request, data, data["serialize"])

    resp = getattr(obj_api, request.method.lower() + '_all')(slug=url, token=token, arg=data, files=files)
    data = resp.json()
    
    try:
        data['status_code'] = resp.status_code
    except TypeError as e:
        print(e)

    return JsonResponse(data, safe=False)

def serialize_keystr_to_json(request, data, key):
    """Funcion para serializar correctamente alguna estructura str to json."""
    if request.method == "POST":
        if key in data:
            data2 = data.copy()
            data_to_convert = data[key]
            json_data = json.loads(data_to_convert)
            data2[key] = json_data
            return data2
    return data          

def clean_data_files(request, data):
    """Funcion para acomodar los files para match en post"""
    if request.method == "POST":
        if 'file' in data:
            data2 = data.copy()
            data_to_convert = data['file']
            json_data = json.loads(data_to_convert)
            data2['file'] = json_data
            return data2
    return data        

        





    # if request.method == "GET":

    #     data = request.GET

    #     if 'url' in data:
    #         url = data['url']
    #     else:
    #         return JsonResponse()

    #     if 'token' in request.session:
    #         token = request.session['token']
    #     else:
    #         token = None

    #     resp = obj_api.get(slug=url, token=token, arg=data)
        
    #     return JsonResponse(resp, safe=False)

    # elif request.method == "POST":
    #     pass

    # elif request.method == "PUT":
    #     data = QueryDict(request.body)
    #     if 'url' in data:
    #         url = data['url']
    #     else:
    #         return JsonResponse()

    #     if 'token' in request.session:
    #         token = request.session['token']
    #     else:
    #         token = None
    #     resp = obj_api.put(slug=url, token=token, arg=data)
        
    #     return JsonResponse(resp, safe=False)
