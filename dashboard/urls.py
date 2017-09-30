from django.conf.urls import url

from . import views

app_name = 'dashboard'

urlpatterns = [


    #url(r'^', views.showList, name='index'),

    #specialists
    url(r'^actor/specialists/$', views.actors.Specialist().showList, name='actor-specialists-list'),
    url(r'^actor/specialists/(?P<specialist_id>[0-9]+)$', views.actors.Specialist().detail, name='actor-specialists-detail'),
    url(r'^actor/specialists/edit/(?P<specialist_id>[0-9]+)$', views.actors.Specialist().edit, name='actor-specialists-edit'),
    url(r'^actor/specialists/create/$', views.actors.Specialist().create, name='actor-specialists-create'),

    #clients
    url(r'^actor/clients/$', views.actors.Client().showList, name='actor-clients-list'),
    url(r'^actor/clients/(?P<client_id>[0-9]+)$', views.actors.Client().showList, name='actor-clients-detail'),
    url(r'^actor/clients/edit/(?P<client_id>[0-9]+)$', views.actors.Client().showList, name='actor-clients-edit'),
    url(r'^actor/clients/create/$', views.actors.Client().showList, name='actor-clients-create'),


    #sellers
    url(r'^actor/sellers/$', views.actors.Seller().showList, name='actor-sellers-list'),
    url(r'^actor/sellers/(?P<seller_id>[0-9]+)$', views.actors.Seller().showList, name='actor-sellers-detail'),
    url(r'^actor/sellers/edit/(?P<seller_id>[0-9]+)$', views.actors.Seller().showList, name='actor-sellers-edit'),
    url(r'^actor/sellers/create/$', views.actors.Seller().showList, name='actor-sellers-create'),

    #administrators
    url(r'^actor/administrators/$', views.actors.Administrator().showList, name='actor-administrators-list'),
    url(r'^actor/administrators/(?P<administrator_id>[0-9]+)$', views.actors.Administrator().showList, name='actor-administrators-detail'),
    url(r'^actor/administrators/edit/(?P<administrator_id>[0-9]+)$', views.actors.Administrator().showList, name='actor-administrators-edit'),
    url(r'^actor/administrators/create/$', views.actors.Administrator().showList, name='actor-administrators-create'),


]