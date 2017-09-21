#from django.contrib.sessions.backends.db import SessionStore
from config import *
import requests
import logging
import pdb #testing

class api:
    _url = CONF_url
    _client_id = CONF_client_id
    _client_secret = CONF_client_secret
    _grant_type = 'password'

    def __init__(self):
        pass

    def token(self,username,password):
        try:
            arg = {'client_id': self._client_id, 'client_secret': self._client_secret, 'grant_type': self._grant_type, 'username': username, 'password': password}
            r = requests.post(self._url+'o/token/', params=arg)
            data = r.json()
            #save session token cokie
            return data
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