from django.conf.urls import url

from . import views

app_name = 'admin'
urlpatterns = [
	url(r'^$', views.Client.showList, name='index'),
    url(r'^admin/client/$', views.Client.showList, name='client-list'),
    url(r'^admin/client/(?P<client_id>[0-9]+)$', views.Client.showClientProfile, name='client-detail'),

]