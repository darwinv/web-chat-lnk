from api.connection import api
from django.contrib.auth import logout

def check_token(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'token' in request.session:
            obj_api = api()
            if not obj_api.check_token(request.session['token'], 'oauth/'):
                logout(request)
            
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware