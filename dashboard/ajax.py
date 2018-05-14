from api.connection import api
from django.http import JsonResponse

def ajax_service(request):
    """Planes Activos."""
    obj_api = api()
    filters = {}

    if 'url' in request.GET:
        url = request.GET['url']
    else:
        return JsonResponse()

    if 'page' in request.GET:
        filters['page'] = request.GET['page']

    if 'token' in request.session:
        token = request.session['token']
    else:
        token = None

    if 'parameters' in request.GET:
        if type(request.GET['parameters']) is dict:
            import pdb
            pdb.set_trace()
            filters = dict(filters, **request.GET['parameters'])

    resp = obj_api.get(slug=url, token=token, arg=filters)
    return JsonResponse(resp)
