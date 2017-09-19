from django.conf.urls import url

from . import views

app_name = 'admin'
urlpatterns = [

    url(r'^$', views.Specialist.showList, name='index'),
    url(r'^actor/$', views.Specialist.showList, name='actor'),
    url(r'^actor/specialist/$', views.Specialist.showList, name='actor-specialist'),

    url(r'^actor/specialist/(?P<specialist_id>[0-9]+)$', views.Specialist.showSpecialistProfile, name='actor-specialist-detail'),


    url(r'^actor/client/(?P<client_id>[0-9]+)$', views.Client.showClientProfile, name='actor-client-detail'),


]