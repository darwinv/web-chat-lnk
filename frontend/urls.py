from django.conf.urls import url

from frontend.views import client, specialist, seller

app_name = 'frontend'

urlpatterns = [

    # frontend
    # aplicacion para visualizar el front de usuarios
    url(r'^client/$', client.Client().index, name='index-client'),
    url(r'^specialist/$', specialist.Specialist().index, name='index-specialist'),
    url(r'^seller/$', seller.Seller().index, name='index-seller'),

]
