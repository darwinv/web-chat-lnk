from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [


    #url(r'^', views.list, name='index'),

    #specialists
    url(r'^actor/specialists/$', views.actors.Specialist().list, name='actor-specialists-list'),
    url(r'^actor/specialists/(?P<specialist_id>[0-9]+)$', views.actors.Specialist().detail, name='actor-specialists-detail'),
    url(r'^actor/specialists/edit/(?P<specialist_id>[0-9]+)$', views.actors.Specialist().edit, name='actor-specialists-edit'),
    url(r'^actor/specialists/create/$', views.actors.Specialist().create, name='actor-specialists-create'),
    url(r'^actor/specialists/delete/$', views.actors.Specialist().delete, name='actor-specialists-delete'),

    #clients
    url(r'^actor/clients/$', views.actors.Client().list, name='actor-clients-list'),
    url(r'^actor/clients/(?P<client_id>[0-9]+)$', views.actors.Client().list, name='actor-clients-detail'),
    url(r'^actor/clients/edit/(?P<client_id>[0-9]+)$', views.actors.Client().list, name='actor-clients-edit'),
    url(r'^actor/clients/create/$', views.actors.Client().list, name='actor-clients-create'),

    #sellers
    url(r'^actor/sellers/$', views.actors.Seller().list, name='actor-sellers-list'),
    url(r'^actor/sellers/(?P<seller_id>[0-9]+)$', views.actors.Seller().list, name='actor-sellers-detail'),
    url(r'^actor/sellers/edit/(?P<seller_id>[0-9]+)$', views.actors.Seller().list, name='actor-sellers-edit'),
    url(r'^actor/sellers/create/$', views.actors.Seller().list, name='actor-sellers-create'),

    #administrators
    url(r'^actor/administrators/$', views.actors.Administrator().list, name='actor-administrators-list'),
    url(r'^actor/administrators/(?P<administrator_id>[0-9]+)$', views.actors.Administrator().list, name='actor-administrators-detail'),
    url(r'^actor/administrators/edit/(?P<administrator_id>[0-9]+)$', views.actors.Administrator().list, name='actor-administrators-edit'),
    url(r'^actor/administrators/create/$', views.actors.Administrator().list, name='actor-administrators-create'),


]