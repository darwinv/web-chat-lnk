#from django.contrib.sessions.backends.db import SessionStore

#project
from api.config import API_URL
from api.config import API_CLIENT_ID
from api.config import API_CLIENT_SECRET
from api.config import API_HEADERS
import requests
import logging
import pdb

#Django
from django.contrib.auth.models import User

class api:
    _url            = API_URL
    _client_id      = API_CLIENT_ID
    _client_secret  = API_CLIENT_SECRET
    _grant_type     = 'password'
    _headers        = API_HEADERS
    def __init__(self, cliente_id=None, client_secret=None, url=None):
        if url:
            self._url = url
        if cliente_id:
            self._client_id = url
        if client_secret:
            self._client_secret = url

    def token(self,username,password):
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
            arg = {'client_id':     self._client_id,\
                   'client_secret': self._client_secret,\
                   'grant_type':    self._grant_type,\
                   'username':      username,\
                   'password':      password,}

            #obtener el token
            r = requests.post(self._url+'o/token/', params=arg, headers=self._headers)
            
            #evaluar respuesta
            if r.status_code == 200:
                #respuesta correcta

                #obtener json como objeto python
                data = r.json()

                #leer y devolver token
                return data['access_token']

            return None

        except Exception as e:
            pass

    def getuserById(self, user_id):
        """

        Requerido por el app login por el uso de la clase de autentitcacion APIBackend

        Usa un identificador unico de usuario para obtener sus datos basicos
        el api debe exponer un servicio para la lista de usuarios
        :param username: username
        :return: usuario
        """

        try:
            #solo para este metodo se va usar un token fijo
            #Django requiere que la clase de autenticacion siempre le devuelva
            #cualquier usuario por id
            headers = {'Authorization': 'Bearer EGsnU4Cz3Mx5bUCuLrc2hmup51sSGz'}
            
            #self._headers.extend(headers)
            self._headers = {'Authorization': 'Bearer ' + token,'x-api-key': 'ebb845f4442a4842aad190f680f731c5'}
            r = requests.get(self._url+'users/' + str(user_id) + '/', headers=self._headers)

            data = r.json()

            user = User()
            user.id = int(data['id'])
            user.username = data['username']

            return user

        except Exception as e:
            pass


    def getUsuario(self, token, username):
        """
        Requerido por el app login por el uso de la clase de autentitcacion APIBackend

        Devuelve un objeto User de la api por medio de un identificador unico

        :param token:token necesario para consultar datos, se utiliza en el header Authorization
        :param user_id: indentificador unico de un usuario en el API
        :return: objeto User
        """

        try:
            headers = {'Authorization': 'Bearer ' + token}

            # print(type(self._headers))
            # print(type(headers))
            # print("------se---------")
            self._headers = {'Authorization': 'Bearer ' + token,'x-api-key': 'ebb845f4442a4842aad190f680f731c5'}

            r = requests.get(self._url+'users?username=' + username, headers=self._headers)

            data = r.json()

            user = User()


            try:
                user.id = int(data[0]['id'])
                user.username = str(data[0]['username'])
            except Exception as e:
                pass

            return user

        except Exception as e:
            pass




    def get(self,arg):

        try:
            self._headers = {'Authorization': 'Bearer YSlqvt8zdSTYaW0sKa2kUJIRN6jTva','x-api-key': 'ebb845f4442a4842aad190f680f731c5'}

            r = requests.get(self._url+arg, headers=self._headers)


            # print(r)
            # print("-------------------------------------------------se----")
            #r = requests.get(self._url, params=arg)
            return r.json()
        except Exception as e:
            pass

    def post(self,arg):
        try:
            payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
            r = requests.get(self._url, params=arg)
            return r.json()
        except Exception as e:
            pass