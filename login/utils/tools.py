from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.utils.six.moves.urllib.parse import urlparse

# Ids Roles de Usuario, pueden ser cargados por bases de datos
ROLE_ADMIN = 1
ROLE_CLIENT = 2
ROLE_SPECIALIST = 3
ROLE_SELLER = 4

def get_app_by_user(role):
    """
    Funcion creada para retornar a que aplicacion debe redirigir cada rol de usuario
    :param role: Int - ID role del usuario
    :return: dict
    """

    if role == ROLE_ADMIN:
        app = {'name':'dashboard', 'url_name':'index'}
    elif role == ROLE_CLIENT:
        app = {'name':'frontend', 'url_name':'index-client'}
    elif role == ROLE_SPECIALIST:
        app = {'name':'frontend', 'url_name':'index-specialist'}
    elif role == ROLE_SELLER:
        app = {'name':'frontend', 'url_name':'index-seller'}
    else:
        app = {'name':'login', 'url_name':'logout'}
            
    return app
    

def role_admin_check():
    """
        return true if user is role ADMIN
    """
    return lambda u: role_check(u, ROLE_ADMIN)

def role_client_check():
    """
        return true if user is role CLIENT
    """
    return lambda u: role_check(u, ROLE_CLIENT)

def role_specialist_check():
    """
        return true if user is role SPECIALIST
    """
    return lambda u: role_check(u, ROLE_SPECIALIST)

def role_seller_check():
    """
        return true if user is role SELLER
    """
    return lambda u: role_check(u, ROLE_SELLER)


def role_check(user, role):
    """
        return true if user is role client
    """
    if user.is_anonymous:
        return False

    return user.role.id == role
