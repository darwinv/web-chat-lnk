from django.conf.urls import url

from . import views

app_name = 'admin'
urlpatterns = [

    #specialists
    url(r'^actor/specialists$', views.showList, name='index'),
    url(r'^actor/specialist/(?P<specialist_id>[0-9]+)$', views.Specialist.showSpecialistProfile, name='actor-specialist-detail'),

    #actors
    url(r'^actor/client/(?P<client_id>[0-9]+)$', views.Client.showClientProfile, name='actor-client-detail'),


]