from django.conf.urls import url

from dashboard.views import actors
app_name = 'seller'

urlpatterns = [

    url(r'^$', actors.Seller().list, name='index'),

]
