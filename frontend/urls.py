"""Urls del Front."""
from django.conf.urls import url
from frontend.views import index, chat, plans, query, contact, match, account, my_account, purchase
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
    # Detalle de plan activo
    url(r'^plans/client/(?P<pk>[0-9]+)/$', plans.Client().plan, name='active-plan'),

    # ACcion de plan activo
    url(r'^plans/client/(?P<pk>[0-9]+)/(?P<action>transfer|empower|share+)/$', plans.Client().action, name='plan-action'),

    # Resumen de plan activo
    url(r'^plans/client/(?P<pk>[0-9]+)/summary/$', plans.Client().summary, name='active-plan-summary'),
    # Resumen de match para especialista
    url(r'^match/specialist/(?P<pk>[0-9]+)/summary/$', match.Specialist().summary, name='match-specialist-summary'),

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


    # Mi Cuenta
    url(r'^myaccount/client/(?P<pk>[0-9]+)/$',
        my_account.Client().account_profile, name='myaccount-client'),

    # url(r'^myaccount/client/edit/(?P<pk>[0-9]+)/$',
    #     my_account.Client().edit_account_profile, name='myaccount-client-edit'),       

    url(r'^contact/linkup/(?P<pk>[0-9]+)/$', my_account.Client().contact_linkup, name='contact-linkup'),
            
    url(r'^myaccount/specialist/(?P<pk>[0-9]+)/$',
        my_account.Specialist().account_profile, name='myaccount-specialist'),

    # Match
    url(r'^match/client/$', match.Client().list_match, name='match-client'),
    url(r'^match/specialist/$', match.Specialist().list_match, name='match-specialist'),
    url(r'^match/client/(?P<pk>[0-9]+)/$', match.Client().detail_match, name='match-client-detail'),
    url(r'^match/client/create/$', match.Client().create_match, name='match-client-create'),
    url(r'^match/specialist/(?P<pk>[0-9]+)/$', match.Specialist().detail_match, name='match-specialist-detail'),


    # Contacto
    url(r'^contact/client/$', contact.Client().contact, name='contact-client'),
    url(r'^contact/specialist/$', contact.Specialist().contact, name='contact-specialist'),


    # Account
    url(r'^account/client/(?P<pk>[0-9]+)/status/$', account.Client().status, name='account-status-client'),
    url(r'^account/specialist/(?P<pk>[0-9]+)/status/$', account.Specialist().status, name='account-status-specialist'),
    url(r'^account/specialist/associates/$', account.Specialist().associates, name='associates-specialist'),

    # Purchase
    url(r'^purchase/client/$', purchase.Client().list_purchase, name='purchase-client'),
    url(r'^purchase/plan/client/$', purchase.Client().list_purchase_plans, name='purchase-plan'),

    # Upload files to query
    url(r'^query/upload_file/$',
        query.upload_file, name='upload_file'),

]
