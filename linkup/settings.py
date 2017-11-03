# -*- coding: utf-8 -*-
"""
Django settings for linkup project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _
import os
from django.db import models
#from linkup.local_settings import *

#import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j+@16&&60x778ef2i9=ae8bfvs_x^v)8d-yoh*2jgv1nsg$%$r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'dashboard.User'
# Application definition

INSTALLED_APPS = [
    'login',
    'dashboard',
    'api',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_ENGINE = "django.contrib.sessions.backends.file"

ROOT_URLCONF = 'linkup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = ['login.APIBackend.APIBackend']

WSGI_APPLICATION = 'linkup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'testLocalDarwin.sqlite3'),
        #'NAME': os.path.join(BASE_DIR, 'testAmazon.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)
# Set the default language for your site.
LANGUAGE_CODE = 'es'

# Tell Django where the project's translation files should be.
LOCALE_PATHS = (    
    os.path.join(BASE_DIR, 'locale/static_db'),   
    os.path.join(BASE_DIR, 'locale'), #python manage.py makemessages -l en
)


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
#Connection credentials
# API_CLIENT_ID = 'NpQiYAbuqisnd2PI65mOVX1eV7kF9WxwowOfOEyv'
# API_CLIENT_SECRET = 'hIfdJUTjiT8FXyxQlp3fmhmkxqIMLiIJ2DsRzgJAGgRUxRgKMkDhZBv2b7Ij5BCFzKeGTNkRg7VloF5bZ87y2Z9D49eN2omXymd0CJCqXOy6UZfhkv2eE0n7TxEMBlHF'
# API_URL = 'http://localhost:7000/'

#from linkup.local_settings import *

