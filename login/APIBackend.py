from api.models import User
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

        # crear objeto api
        obj_api = api()

        # validar datos por medio de una consulta del token del usuario
        token = obj_api.token(request.POST['user'], request.POST['password'])

        # validar respuesta
        if token:
            # existe token

            # guardar token en la sesion
            request.session['token'] = token
            
            try:
                # se debe pasar user y token para obtener los datos del usuario
                user = obj_api.getUsuario(token, username)
                # guardar usuario unicamete para que el framework acepte el objeto
                user.save()

                # Si es role especialista
                if user.role.id==3:
                    specialist = obj_api.get_all(token, slug="specialists-users/{}/".format(username))
                    
                    if specialist.status_code == 200:
                        data_specialist = specialist.json()
                        request.session['specialist'] = {}
                        request.session['specialist']['type_specialist'] = data_specialist['type_specialist']

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

        try:
            obj_api = api()
            # consultar un usuario por el identificador unico
            return obj_api.getuserById(user_id)

        except User.DoesNotExist:
            return None
