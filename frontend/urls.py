from django.conf.urls import url

from frontend.views import client, specialist, seller

app_name = 'frontend'

urlpatterns = [

    # frontend
    # aplicacion para visualizar el front de usuarios
    url(r'^client/$', client.Client().tempPage, name='temp-page-client'),
    url(r'^specialist/$', specialist.Specialist().tempPage, name='temp-page-specialist'),
    url(r'^seller/$', seller.Seller().tempPage, name='temp-page-seller'),

]
