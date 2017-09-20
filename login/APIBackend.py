from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from api.connection import api

class APIBackend(object):
    """
    """

    def authenticate(self, request, username=None, password=None):
        """
        A partir de la respuesta se obtiene el usuario por medio
        del nombre de usuario
        :param request:
        :param username:
        :param password:
        :return:
        """
        print "authenticate"
        print request.POST

        apiObj = api()
        token = apiObj.token(request.POST['user'], request.POST['password'])

        if token:
            print "if token " + token

            # guardar token
            request.session['token'] = token
            try:
                #se debe pasar unicamente user y token
                #user = apiObj.getUsuario(token, request.POST['user'])
                user = apiObj.getUsuario(token, username)
                user.save()

            except User.DoesNotExist:
                return None

            return user
        return None

    def get_user(self, user_id):
        print "APIBackend get_user"
        print user_id
        try:
            apiObj = api()
            return apiObj.getuserById(user_id)
        except User.DoesNotExist:
            return None