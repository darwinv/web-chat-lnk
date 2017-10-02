from django.conf import settings
from django.contrib.auth.hashers import check_password
#from django.contrib.auth.models import User
from dashboard.models import User
from api.connection import api

class APIBackend(object):
    """
    """

    def authenticate(self, request, username=None, password=None):
        """
        A partir del nombre de usuario y password se comprueba
        si son los datos correctos por medio de una consulta al api linkup

        :param request: request con los datos de username y password
        :param username: identificador unico del usuario
        :param password: clave del usuario
        :return: objeto User si existe el usuario o None si no existe o el password es incorrecto
        """

        #print "authenticate"
        #print request.POST

        #crear objeto api
        apiObj = api()
        
        #validar datos por medio de una consulta del token del usuario
        token = apiObj.token(request.POST['user'], request.POST['password'])

        #validar respuesta
        if token:
            #existe token

            #print "if token " + token

            # guardar token en la sesion
            request.session['token'] = token

            try:
                #se debe pasar user y token para obtener los datos del usuario
                user = apiObj.getUsuario(token, username)
                #guardar usuario unicamete para que el framework acepte el objeto
                
                user.save()

            except User.DoesNotExist:
                return None

            return user
        return None

    def get_user(self, user_id):
        """
        Django exige a la clase de autenticacion un metodo
        para obtener cualquier usuario por el identificador unico

        :param user_id: identificador unico del usuario
        :return: objeto User o None
        """
        #print "APIBackend get_user"
        #print user_id

        try:
            apiObj = api()
            #consultar un usuario por el identificador unico
            return apiObj.getuserById(user_id)

        except User.DoesNotExist:
            return None