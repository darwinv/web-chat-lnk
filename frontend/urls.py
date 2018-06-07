"""Urls del Front."""
from django.conf.urls import url
from frontend.views import client, specialist, seller, query
from login.utils.tools import get_app_by_user

app_name = 'frontend'

urlpatterns = [
    # frontend
    # aplicacion para visualizar el front de usuarios
    # -----------------------------------------------
    # Urls de Cliente
    url(r'^client/$', client.Client().index, name='index-client'),
    url(r'^client/chat/(?P<pk>[0-9]+)/$', client.Client().chat,
        name='chat-client'),
    # cambiar plan elegido
    url(r'^client/chosenplan/(?P<pk>[0-9]+)/$', client.set_chosen_plan,
        name='set-chosen-plan'),
    # Activar plan
    url(r'^client/plans/activate/(?P<code>[0-9a-zA-Z]+)/$',
        client.activate_plan,
        name='activate-plan'),
    # Lista de Planes activos
    url(r'^client/plans/$', client.plans, name='active-plans'),
    # Lista de planes por activar por codigo PIN
    url(r'^client/pincode/plans/(?P<code>[0-9a-zA-Z]+)/$',
        client.get_plans_code,
        name='pincode-plans'),
    # Enviar consulta cliente
    url(r'^client/query/$',
        client.send_query,
        name='send-query'),
    # Urls de Especialista
    url(r'^specialist/$', specialist.Specialist().index,
        name='index-specialist'),
    url(r'^specialist/chat/(?P<pk>[0-9]+)/$', specialist.Specialist().chat,
        name='chat-specialist'),
    # Urls del Vendedor
    url(r'^seller/$', seller.Seller().index, name='index-seller'),

    # Upload files to query
    url(r'^query/upload_file/$',
        query.upload_file, name='upload_file'),
]
