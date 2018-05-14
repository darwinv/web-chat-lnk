from django.conf.urls import url

from dashboard.views import actors, account, account_status, authorizations
from dashboard import ajax

app_name = 'dashboard'

urlpatterns = [

    url(r'^$', actors.Specialist().list, name='index'),

    # specialists
    url(r'^actor/specialists/$', actors.Specialist().list, name='actor-specialists-list'),
    url(r'^actor/specialists/(?P<pk>[0-9]+)$', actors.Specialist().detail, name='actor-specialists-detail'),
    url(r'^actor/specialists/edit/(?P<pk>[0-9]+)$', actors.Specialist().edit, name='actor-specialists-edit'),
    url(r'^actor/specialists/create/$', actors.Specialist().create, name='actor-specialists-create'),
    url(r'^actor/specialists/delete/$', actors.Specialist().delete, name='actor-specialists-delete'),

    # clients
    url(r'^actor/clients/$', actors.Client().list, name='actor-clients-list'),
    url(r'^actor/clients/(?P<pk>[0-9]+)$', actors.Client().detail, name='actor-clients-detail'),
    url(r'^actor/clients/edit/(?P<pk>[0-9]+)$', actors.Client().edit, name='actor-clients-edit'),
    url(r'^actor/clients/create/$', actors.Client().create, name='actor-clients-create'),
    url(r'^actor/clients/delete/$', actors.Client().delete, name='actor-clients-delete'),

    # sellers
    url(r'^actor/sellers/$', actors.Seller().list, name='actor-sellers-list'),
    url(r'^actor/sellers/(?P<pk>[0-9]+)$', actors.Seller().detail, name='actor-sellers-detail'),
    url(r'^actor/sellers/edit/(?P<pk>[0-9]+)$', actors.Seller().edit, name='actor-sellers-edit'),
    url(r'^actor/sellers/create/$', actors.Seller().create, name='actor-sellers-create'),

    # administrators
    url(r'^actor/administrators/$', actors.Administrator().list, name='actor-administrators-list'),
    url(r'^actor/administrators/(?P<pk>[0-9]+)$', actors.Administrator().list, name='actor-administrators-detail'),
    url(r'^actor/administrators/edit/(?P<pk>[0-9]+)$', actors.Administrator().list, name='actor-administrators-edit'),
    url(r'^actor/administrators/create/$', actors.Administrator().list, name='actor-administrators-create'),

    # Autorizaciones
    url(r'^authorizations/clients$', authorizations.AutorizationClient().list, name='authorizations-clients'),

    # Estados de cuenta
    url(r'^account_status/sellers/$', account_status.AccountStatusSeller().list, name='account-status-seller'),

    # Ajax Service
    url(r'^ajax_service/$', ajax.ajax_service, name='ajax-service'),
]
