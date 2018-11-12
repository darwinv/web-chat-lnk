"""Urls del Front."""
from django.conf.urls import url
from frontend.views import index, chat, plans, query, contact, match
from login.utils.tools import get_app_by_user

app_name = 'frontend'

urlpatterns = [
    # frontend
    # aplicacion para visualizar el front de usuarios
    # -----------------------------------------------

    # Indexes
    url(r'^client/$', index.Client().index, name='index-client'),
    url(r'^specialist/$', index.Specialist().index, name='index-specialist'),
    url(r'^seller/$', index.Seller().index, name='index-seller'),
    

    # Plans
    # cambiar plan elegido
    url(r'^plans/client/chosenplan/(?P<pk>[0-9]+)/$', plans.Client().set_chosen_plan,
        name='set-chosen-plan'),
    # Activar plan
    url(r'^plans/client/activate/(?P<code>[0-9a-zA-Z]+)/$', plans.Client().activate_plan,
        name='activate-plan'),
    # Lista de Planes activos
    url(r'^plans/client/$', plans.Client().plans, name='active-plans'),
    # Lista de planes por activar por codigo PIN
    url(r'^plans/client/pincode/(?P<code>[0-9a-zA-Z]+)/$', plans.Client().get_plans_code,
        name='pincode-plans'),
   # Chequeo de Status de Planes   
   url(r'^plans/status/$', plans.Client().get_status_footer,
        name='status-footer-plans'),
    # Chat
    url(r'^chat/client/(?P<pk>[0-9]+)/$', chat.Client().chat,
        name='chat-client'),
    # Enviar consulta clientec
    url(r'^chat/client/query/$', chat.Client().send_query, name='send-query'),
    url(r'^chat/specialist/(?P<pk>[0-9]+)/$', chat.Specialist().chat,
        name='chat-specialist'),

    # Match
    url(r'^match/client/$', match.Client().list_match, name='match-client'),

    # Contacto
    url(r'^contact/client/$', contact.Client().contact, name='contact-client'),
    url(r'^contact/specialist/$', contact.Specialist().contact, name='contact-specialist'),


    # Upload files to query
    url(r'^query/upload_file/$',
        query.upload_file, name='upload_file'),
]
