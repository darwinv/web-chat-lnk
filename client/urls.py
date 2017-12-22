from django.conf.urls import url

from dashboard.views import actors
app_name = 'client'

urlpatterns = [

    url(r'^$', actors.Client().list, name='index'),
    
]
