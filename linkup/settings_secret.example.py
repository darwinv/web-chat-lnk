"""Archivo de ejemplo para configurar la bd en local."""
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'testLocalDarwin.sqlite3'),
    }
}

# CONFIG_LOCAL
CONFIG_ENVIROMENT = {
    "apiKey": "AIzaSyDFLaQvnBi43cAYnbbIJYM5d8HhjlWuMFw",
    "authDomain": "linkup-local.firebaseapp.com",
    "databaseURL": "https://linkup-local.firebaseio.com",
    "projectId": "linkup-local",
    "storageBucket": "linkup-local.appspot.com",
    "messagingSenderId": "901859853311"
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'web',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# CONFIG_PROD = {
#     "apiKey": 'AIzaSyB8dhD2VmGvfsdfs0BHew88VOVTU',
#     "authDomain": 'linkup-pdion-9qddqwdaf.firebaseapp.com',
#     "databaseURL": 'https://linkdaupan-92f.firebaseio.com',
#     "projectId": 'linkqweduction-qe8af',
#     "storageBucket": 'linkuqwen-978af.aqeot.com',
#     "messagingSenderId": '34234235337'
# }
#
# #definimos a la variable config_enviroment el entorno que apuntara el proyecto
# CONFIG_ENVIROMENT = CONFIG_LOCAL