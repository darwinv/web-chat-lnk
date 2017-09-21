#from django.contrib.sessions.backends.db import SessionStore
import requests
import logging
import pdb #testing

class api:
    _url = 'http://localhost:3000/'
    _client_id = 'FUN5EkBDdiQo8SixJYslF41ZkrjAhQtWKkV7BEE2'
    _client_secret = 'P7pj3QcE6GyhlS0QUzJOJ8SRLlTGHYSMESGr7QzlyKnuMsc4osaaStB6wSiGGxAelKjXv6xJ7p9Go8R5el2KaVlcM4P50IeplkY2CWHxaOc9NI1fLKS9DoWxD9UbG4TN'
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