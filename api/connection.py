# from django.contrib.sessions.backends.db import SessionStore

# project
from api.config import API_URL, API_CLIENT_ID, API_CLIENT_SECRET, API_HEADERS
import requests
from django.utils import translation
from django.urls import reverse
import pdb
from django.http import HttpResponseRedirect
# Django
# from django.contrib.auth.models import User
from api.models import User, Role


# noinspection PyPep8Naming
class api:
    _url = API_URL
    _client_id = API_CLIENT_ID
    _client_secret = API_CLIENT_SECRET
    _grant_type = 'password'
    _headers = API_HEADERS

    _language = 'es'

    def __init__(self, cliente_id=None, client_secret=None, url=None, language=None):
        if url:
            self._url = url
        if cliente_id:
            self._client_id = cliente_id
        if client_secret:
            self._client_secret = client_secret

        if language:
            self._language = language
        else:
            cur_language = translation.get_language()
            self._language = cur_language

    def token(self, username, password):
        """
        Requerido por el app login por el uso de la clase de autentitcacion APIBackend
        Autentica el usuario con el API, si el usuario y la contrasena
        son correctas el api devuelve token, refresh token y fecha de expiracion
        de los mismos.

        :param username: nombre de usuario
        :param password: contrasena del usuario
        :return: token
        """

        try:
            arg = {'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'grant_type': self._grant_type,
                   'username': username,
                   'password': password,
                   }

            # obtener el token
            r = requests.post(self._url + 'o/token/', params=arg, headers=self._headers)

            print(r.json())
            print("--------------LOGIN------------------")
            # evaluar respuesta
            if r.status_code == 200:
                # respuesta correcta

                # obtener json como objeto python
                data = r.json()

                # leer y devolver token
                return data['access_token']

            return None

        except Exception as e:
            print(e.args)
            print("---------------ERROR TOKEN---------------")

    def getuserById(self, user_id):
        """

        Requerido por el app login por el uso de la clase de autentitcacion APIBackend

        Usa un identificador unico de usuario para obtener sus datos basicos
        el api debe exponer un servicio para la lista de usuarios
        :param user_id: user_id
        :return: usuario
        """

        try:
            # solo para este metodo se va usar un token fijo
            # Django requiere que la clase de autenticacion siempre le devuelva
            # cualquier usuario por id
            # headers = {'Authorization': 'Bearer EGsnU4Cz3Mx5bUCuLrc2hmup51sSGz'}

            # self._headers.extend(headers)
            # Ubicar el uso del token estatico en la configuracion
            # Esta metodo requerido por el framework siempre debe poder
            # acceder a los usuarios, siempre usa el mismo token
            # usar git diff para ver diferencias y encontra los bugs

            headers = {'Authorization': 'Bearer EGsnU4Cz3Mx5bUCuLrc2hmup51sSGz'}

            headers = dict(headers, **self._headers)

            r = requests.get(self._url + 'users/' + str(user_id) + '/', headers=headers)

            data = r.json()

            # obtener id de la respuesta
            pk = int(data['id'])

            user = None
            if User.objects.filter(id=pk).count() > 0:
                user = User.objects.filter(id=pk)[0]

            # evaluar si existe el usuario en las sesiones guardadas
            if user:
                user.username = str(data['username'])
            else:
                user = User()
                user.id = pk
                user.username = str(data['username'])

            return user

        except Exception as e:
            pass

    def getUsuario(self, token, username):
        """
        Requerido por el app login por el uso de la clase de autentitcacion APIBackend

        Devuelve un objeto User de la api por medio de un identificador unico

        :param token: token necesario para consultar datos, se utiliza en el header Authorization
        :param user_id: indentificador unico de un usuario en el API
        :return: objeto User
        """

        try:
            headers = {'Authorization': 'Bearer ' + token}

            headers = dict(headers, **self._headers)

            r = requests.get(self._url + 'users?username=' + username, headers=headers)
            
            data = r.json()
            try:
                # obtener id de la respuesta

                id = int(data['results'][0]['id'])

                                    
                # evaluar si existe el usuario en las sesiones guardadas
                if User.objects.filter(id=id).count() > 0:
                    user = User.objects.filter(id=id)[0]
                else:
                    user = User()

                # Se agregan campos necesarios en base de datos local
                # tomando en cuenta campos requeridos y unicos
                user.id = id
                user.username = str(data['results'][0]['username'])
                user.code = str(data['results'][0]['code'])
                user.document_number = str(data['results'][0]['document_number'])
                user.email_exact = str(data['results'][0]['email_exact'])

                role_id = int(data['results'][0]['role'])
                user.role.id = user.role.pk = role_id
                role = Role.objects.get(pk=role_id)
                user.role.name = role.name


            except Exception as e:
                print(e)
                print("---------------ERROR GETUSER---------------")

            return user

        except Exception as e:
            pass

    def logout(self, token):
        headers = {'Authorization': 'Bearer ' + token, 'Accept-Language': self._language}
        headers = dict(headers, **self._headers)
        slug = 'o/revoke_token/'
        arg = {
            "token": token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            }

        try:
            return requests.post(self._url + slug, headers=headers, params=arg)
        except Exception as e:
            print(e.args)
            print("---------------ERROR LOGOUT---------------")


    def get(self, token, slug='', arg=None, ):

        try:

            headers = {'Authorization': 'Bearer ' + token}

            headers = dict(headers, **self._headers)
            r = requests.get(self._url + slug, headers=headers, params=arg)

            if r.status_code == 401:
                #logout = requests.get(reverse('login:logout'))
                #return HttpResponseRedirect(reverse('login:logout'))
                print("---------------401resp---------------------")
            else:
                return r.json()

        except Exception as e:
            print(e.args)
            print("---------------ERROR GET---------------")

    def post(self, token='', slug='', arg=None, files=None):
        headers = {'Accept-Language': self._language}
        
        if token:
            headers['Authorization'] = 'Bearer {}'.format(token)
            headers = dict(headers, **self._headers)
        try:
            r = requests.post(self._url + slug, headers=headers, json=arg, files=files)
            return r.json()
            
        except Exception as e:
            print(e.args)
            print("---------------ERROR POST---------------")

    def put(self, token, slug='', arg=None, files=None):
        headers = {'Authorization': 'Bearer ' + token}
        headers = dict(headers, **self._headers)

        try:
            r = requests.put(self._url + slug + '/', headers=headers, json=arg, files=files)            
            
            return r.json()
            
        except Exception as e:
            print(e)
            print("---------------ERROR PUT---------------")

    def delete(self, token, slug='', arg=None):
        headers = {'Authorization': 'Bearer ' + token}
        headers = dict(headers, **self._headers)

        try:
            r = requests.delete(self._url + slug, headers=headers, params=arg)

            return r.json()
        except Exception as e:
            print(e)
            print("---------------ERROR DELETE---------------")
