"""Urls del Front."""
from django.conf.urls import url
from frontend.views import client, specialist, seller

app_name = 'frontend'

urlpatterns = [

    # frontend
    # aplicacion para visualizar el front de usuarios
    # -------------------------------------------------
    # Urls de Cliente
    url(r'^client/$', client.Client().index, name='index-client'),
    url(r'^client/chat/(?P<pk>[0-9]+)/$', client.Client().chat, name='chat-client'),
    # Urls de Especialista
    url(r'^specialist/$', specialist.Specialist().index, name='index-specialist'),
    url(r'^seller/$', seller.Seller().index, name='index-seller'),

]
