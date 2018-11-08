from api.connection import api
from django.http import JsonResponse
from django.http import QueryDict

def ajax_service(request):
    """Planes Activos."""
    obj_api = api()
    if request.method == "GET":

        filters = request.GET

        if 'url' in request.GET:
            url = request.GET['url']
        else:
            return JsonResponse()

        if 'token' in request.session:
            token = request.session['token']
        else:
            token = None

        resp = obj_api.get(slug=url, token=token, arg=filters)
        
        return JsonResponse(resp, safe=False)

    elif request.method == "POST":
        pass

    elif request.method == "PUT":
        data = QueryDict(request.body)
        if 'url' in data:
            url = data['url']
        else:
            return JsonResponse()

        if 'token' in request.session:
            token = request.session['token']
        else:
            token = None

        resp = obj_api.put(slug=url, token=token, arg=data)
        
        return JsonResponse(resp, safe=False)
