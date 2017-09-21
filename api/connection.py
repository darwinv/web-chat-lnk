#from django.contrib.sessions.backends.db import SessionStore
from config import *
import requests
import logging
import pdb

#Django
from django.contrib.auth.models import User

class api:
    _url = 'http://localhost:7000/'
    _client_id = 'NpQiYAbuqisnd2PI65mOVX1eV7kF9WxwowOfOEyv'
    _client_secret = 'hIfdJUTjiT8FXyxQlp3fmhmkxqIMLiIJ2DsRzgJAGgRUxRgKMkDhZBv2b7Ij5BCFzKeGTNkRg7VloF5bZ87y2Z9D49eN2omXymd0CJCqXOy6UZfhkv2eE0n7TxEMBlHF'
    _grant_type = 'password'

    def __init__(self, cliente_id, client_secret, url):
        self._url = url
        self._client_id = cliente_id
        self._client_secret = client_secret

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
                   'password':      password}

            #obtener el token
            r = requests.post(self._url+'o/token/', params=arg)

            #evaluar respuesta
            if r.status_code == 200:
                #respuesta correcta

                #obtener json como objeto python
                data = r.json()

                #leer y devolver token
                return data['access_token']

            return None

        except Exception as e:
            #registrar error
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)

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
            r = requests.get(self._url+'users/' + str(user_id) + '/', headers=headers)

            data = r.json()

            user = User()
            user.id = int(data['id'])
            user.username = data['username']

            return user

        except Exception as e:
            print e
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)


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
            r = requests.get(self._url+'users?username=' + username, headers=headers)

            data = r.json()

            user = User()

            try:
                user.id = int(data[0]['id'])
                user.username = str(data[0]['username'])

            except Exception as e:
                print e

            return user

        except Exception as e:
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)

    def get(self,arg):
        try:
            r = requests.get(self._url+arg)
            #r = requests.get(self._url, params=arg)
            return r.json()
        except Exception as e:
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)

    def post(self,arg):
        try:
            payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
            r = requests.get(self._url, params=arg)
            return r.json()
        except Exception as e:
            logging.basicConfig(filename='logging.log',level=logging.DEBUG)
            logging.error(e)