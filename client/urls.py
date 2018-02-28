from django.conf.urls import url

from dashboard.views import actors
from client.views import views

app_name = 'client'

urlpatterns = [
    url(r'^$', views.tempPage, name='index'),
]
