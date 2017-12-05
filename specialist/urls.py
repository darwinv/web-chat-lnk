from django.conf.urls import url

from dashboard.views import actors
app_name = 'specialist'

urlpatterns = [

    url(r'^$', actors.Specialist().list, name='index'),

]
