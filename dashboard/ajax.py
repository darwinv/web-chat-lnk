from api.connection import api
from django.http import JsonResponse

def ajax_service(request):
    """Planes Activos."""
    obj_api = api()
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
